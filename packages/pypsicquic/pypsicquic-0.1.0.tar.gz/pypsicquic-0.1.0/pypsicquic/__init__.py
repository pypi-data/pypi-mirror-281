import xml.etree.ElementTree as ET
import requests
from sys import stderr
import networkx as nx
import re

class Dtree:
    def __init__(self):
        self.data = {}
    def add(self, a, b):
        for _ in (a,b):
            if not _ in self.data:
                self.data[_] = set([])
        self.data[a].add(b)
        self.data[b].add(a)
    def __getitem__(self, k):
        return self.data[k]

    def __bool__(self): 
        return bool(self.data)
    
    
class PsicquicStore:
    def __init__(self, xml_file="registry.xml", proxy = None):
        self._registry_url = url_registry = 'http://www.ebi.ac.uk/Tools/webservices/psicquic/registry/registry?action=ACTIVE&format=xml'
        
        self.proxies = proxy
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ns = '{http://hupo.psi.org/psicquic/registry}'
        self.services = { s.find(f"{ns}name").text : s.find(f"{ns}restUrl").text.replace(' ', '') \
                         for s in root.findall(f"{ns}service")\
                        }
        self.curr_endpoint =  self.services['IntAct']
    def set_service(self, service_id, mute=False):
        if not service_id in self.services:
            raise ValueError(f"{service_id} not a valid provider")
        
        self.curr_endpoint = self.services[service_id]
        if not mute :
            print(f"Active url set to {self.curr_endpoint}", file=stderr)

    def find_source(self, **kwargs):
        """ Test each service for a non empty response on asked miql query
        """
        furbished_service = []
        for service_id in self.services:
            self.set_service(service_id, mute=True)
            maybe_psq_view =  self.get(mute=True, **kwargs)
            if maybe_psq_view:
                furbished_service.append( (service_id, len(maybe_psq_view)) )
        return furbished_service

    def _urlget(self, url):
        resp = requests.get(url, proxies=self.proxies)
        if not resp.ok:
            raise ValueError(f"Url Fetching error {resp.status_code} at {url}")
        return resp
        
    def get(self, mute = False, **kwargs):
        if "pmid" in kwargs:
            url = f"{self.curr_endpoint}query/pubmed:{kwargs['pmid']}"
            if not mute:
                print(url, file=stderr)
            ans = self._urlget(url)
            if not ans.text:                
                return None
            return PsicquicView(raw=ans.text)
        ## too long
        """
        if "species" in kwargs:
            url = f"{self.curr_endpoint}query/species:{kwargs['species']}"
            print(url, file=stderr)
            ans = self._urlget(url)
            return self.viewer(ans.text)
        """
    def get_from(self, mol_ids, steps=1):
        """ Build the PsicquicView for the partners of the provided proteins
        The steps parameter controls the diameter of the partners shells, the depth of the search.
        By default steps equals 1, which retuns only the 1st neighbours of the input proteins.
        """
        mitab_set = self._get_from(set(mol_ids), set(), set(), steps - 1)
        return PsicquicView(psq_datum_iter=mitab_set)
    
    def _get_from(self, mol_ids, prev_mol_ids, psq_datum_set, steps):
        def get_psq_datum_set(url):
            print(url)
            ans = self._urlget(url)
            return set([ PsicquicDatum(l.split("\t")) for l in ans.text.split("\n") if l ])
        def chunks(xs, n):
            xs = list(xs)
            n = max(1, n)
            return (xs[i:i+n] for i in range(0, len(xs), n))
        
        # exclude partners already known
        black = Dtree()
        for psq_datum in psq_datum_set:
            e = psq_datum.interactors
            black.add(*e)
        # collect new interactions
        maybe_new_psq_datum = set()
        for mol_id in mol_ids:
            if not black:
                url = f"{self.curr_endpoint}query/id:{mol_id}"
                maybe_new_psq_datum |= get_psq_datum_set(url)
                continue
                
            for black_mol_ids in chunks(black[mol_id], 40):
                url = f"{self.curr_endpoint}query/id:{mol_id} AND NOT ({' OR '.join(black_mol_ids)})"
                maybe_new_psq_datum |= get_psq_datum_set(url)
                    
        # They should all be new   
        #new_psq_datum = maybe_new_psq_datum - psq_datum_set
        new_psq_datum = maybe_new_psq_datum
        if not new_psq_datum or steps == 0:
            return new_psq_datum
        
        # We could circle back to already knew molecules
        maybe_new_mol_ids = set()
        for psq_datum in new_psq_datum:
            maybe_new_mol_ids.update(psq_datum.interactors)
        new_mol_ids = maybe_new_mol_ids - mol_ids
        print(f"search countdown {steps}, new molecule/interaction counts = {len(list(new_mol_ids))} {len(list(new_psq_datum))}")
        next_new_psq_datum = \
            self._get_from(new_mol_ids,  prev_mol_ids | mol_ids, new_psq_datum | psq_datum_set, steps - 1)
        return next_new_psq_datum | new_psq_datum
        

class PsicquicView:
    def __init__(self, raw=None, io_wrapper=None, psq_datum_iter = None):
        assert raw or psq_datum_iter or io_wrapper
        if io_wrapper:
            self.data = [ PsicquicDatum(l.replace("\n", "").split("\t")) for l in io_wrapper ]
        elif raw:
            self.data = [ PsicquicDatum(l.split("\t")) for l in raw.split("\n") ]
        else:
            self.data = [ _ for _ in psq_datum_iter]
        
    def __iter__(self):
        for psq_datum in self.data:
            yield(psq_datum)

    def __str__(self):
        return '\n'.join([str(_) for _ in self.data])
    
    def __getitem__(self, _slice):
        _ = self.data[_slice]
        return PsicquicView(psq_datum_iter=_)

    def __repr__(self):
        return str(self)
    def __len__(self):
        return len(self.data)
    def filter(self, physical_only=True):
        _ = [ psicquic_datum for psicquic_datum in self.data if psicquic_datum.is_physical ]
        return PsicquicView(psq_datum_iter=_)
        
    
class PsicquicDatum:
    def __init__(self, mitab_line_array):
        self._data = mitab_line_array
    def __getitem__(self, i):
        return self._data[i]
    
    @property
    def interactors(self):
        return (self._data[0], self._data[1]) \
                    if self._data[0] > self._data[1] \
                    else (self._data[1], self._data[0])
    def __hash__(self): 
        #(iA, iB) = self.interactors
        #return hash( iA + iB )
        return hash(''.join(self._data))
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __ne__(self, other):
        return hash(self) != hash(other)
    def __str__(self):
        return "\t".join(self._data)
    def __repr__(self):
        return str(self)
    @property
    def is_physical(self):
        if len(self._data) >= 12:
            return self._data[11] == "psi-mi:\"MI:0915\"(physical association)"
        return False
    
class PsicquicNetwork:
    def __init__(self):
        pass

    def load_psq(self, psq_datum_iter):        
        self.G = nx.Graph()
        for psq_datum in psq_datum_iter:
            node_pair = psq_datum.interactors
            if not self.G.has_edge(*node_pair):
                self.G.add_edge(*node_pair, psq_data=[])
            self.G[ node_pair[0] ][ node_pair[1] ]['psq_data'].append(psq_datum)
    
    def load_nx(self, G):
        self.G = G
    
    def find_nodes(self, expr):
        re_pattern = re.compile(expr)
        return [ n for n in self.G.nodes if re_pattern.match(str(n)) ]

    def _subgraph(self, prev_nodes, c_nodes, left):
        new_nodes = []
        # get the new neighbourhood
        for nc in c_nodes:
            for nn in self.G.neighbors(nc):
                if not (nn in prev_nodes or nn in c_nodes):
                    new_nodes.append(nn)
        # stop condition
        if not new_nodes or left == 1:
            return new_nodes
        # calling next expansion, w/ curr_nodes passed into previous and new neighbours as seed for next search
        next_new = self._subgraph( prev_nodes + c_nodes, new_nodes, left-1)
        return new_nodes + next_new
    
    def subgraph(self, central_node_list, degree=1):
        # could use https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.degree.html
        # to ctrl degree value
        seed_nodes =  [ _ for _ in central_node_list ]
        new_nodes  = self._subgraph([], seed_nodes, degree )
        new_self   = PsicquicNetwork()
        new_self.load_nx(self.G.subgraph( seed_nodes + new_nodes) )
        return new_self
    
    def del_nodes(self, nx_nodes):
        self.G.remove_nodes_from(nx_nodes)
    