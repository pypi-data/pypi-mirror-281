
class Panlex (object):

    
    
#     def get_header (self, fname):
#         with open(join(self.csvdir, fname)) as f:
#             return next(f).rstrip('\r\n').split(',')
# 
#     def schema (self):
#         for name in listdir(self.csvdir):
#             if name.endswith('.csv'):
#                 yield (name[:-4], self.get_header(name))
# 
#     def lvtab (self):
#         if self._lvtab is None:
#             self._read_lvtab()
#         return self._lvtab
# 
#     def _read_lvtab (self):
#         self._lvtab = tab = {}
#         with open(join(self.tgtdir, 'langvar.csv')) as f:
#             r = csv.reader(f)
#             if next(r) != ['id', 'lang_code', 'var_code', 'mutable', 'name_expr',
#                            'script_expr', 'meaning', 'region_expr', 'uid_expr', 'grp']:
#                 raise Exception('File format has changed')
#             for fields in r:
#                 lv = Variety()
#                 lv.lvid = fields[0]
#                 lv.lang_code = fields[1]
#                 lv.var_code = fields[2]
#                 lv.mutable = fields[3]
#                 lv.name = fields[4]
#                 lv.script = fields[5]
#                 lv.meaning = fields[6]
#                 lv.region = fields[7]
#                 lv.uid = fields[8]
#                 lv.grp = fields[9]
#                 tab[lv.lvid] = lv
    
#     def lang_varieties (self, lang_code):
#         for lv in self.lvtab().values():
#             if lv.lang_code == lang_code:
#                 yield lv
#     
#     def lang_variety (self, lang_code, var_code):
#         for lv in self.lvtab().values():
#             if lv.lang_code == lang_code and lv.var_code == var_code:
#                 return lv
    
    def print_lvid (self, lvid):
        lvtab = self.lvtab()
        lvtab[lvid].pprint()

    def print_var (self, lang_code, var_code):
        self.lang_variety(lang_code, var_code).pprint()

    def print_lang (self, lang_code):
        vars = sorted(self.lang_varieties(lang_code), key=lambda lv: lv.uid)
        for lv in vars:
            lv.pprint()
            print()

    def dtab (self):
        if self._dtab is None:
            self._read_dtab()
        return self._dtab

    def _read_dtab (self):
        tab = self._dtab = {}
        with open(join(self.tgtdir, 'dicts.tab')) as f:
            for line in f:
                r = line.rstrip('\r\n').split('\t')
                d = Dictionary()
                d.id = r[0]
                d.reg_date = r[1]
                d.label = r[2]
                d.url = r[3]
                d.isbn = r[4]
                d.author = r[5]
                d.title = r[6]
                d.publisher = r[7]
                d.year = r[8]
                d.quality = r[9]
                d.grp = r[10]
                d.note = r[11]
                d.license = r[12]
                d.ip_claim = r[13]
                d.ip_claimant = r[14]
                d.ip_claimant_email = r[15]
                tab[d.id] = d

    def print_dictionary (self, sid):
        d = self.dtab()[sid]
        print('id', d.id)
        print('reg_date', d.reg_date)
        print('label', d.label)
        print('url', d.url)
        print('isbn', d.isbn)
        print('author', d.author)
        print('title', d.title)
        print('publisher', d.publisher)
        print('year', d.year)
        print('quality', d.quality)
        print('grp', d.grp)
        print('note', d.note)
        print('license', d.license)
        print('ip_claim', d.ip_claim)
        print('ip_claimant', d.ip_claimant)
        print('ip_claimant_email', d.ip_claimant_email)


class Installer (object):
    

#     def variety_dicts (self, lv):
#         idx = self.source_langvar()
#         return [r.source for r in idx[lv]]
#         
#     def source_langvar (self):
#         if self._source_langvar is None:
#             csv = self.csv()
#             tab = csv['source_langvar']
#             self._source_langvar = Index(tab, 'langvar', multi=True)
#         return self._source_langvar

#     def varieties (self):
#         fn = join(self.tgtdir, 'varieties')
#         if exists(fn):
#             print('Already installed')
#         else:
#             print('Installing', fn)
#             self.need_tgtdir()
#             with open(fn, 'w') as f:
#                 first = True
#                 for (lvid, lang_code, var_code, mutable, name, script, _, region, uid, grp) \
#                     in self.csv['langvar'].rows:
#                     name = self.expr(name)
#                     script = self.expr(script)
#                     region = self.expr(region)
#                     uid = self.expr(uid)
# 
#                     if first: first = False
#                     else: print(file=f)
#                     print('id', lvid, file=f)
#                     print('lg', lang_code, file=f)
#                     print('va', var_code, file=f)
#                     print('mu', mutable, file=f)
#                     print('na', name, file=f)
#                     print('sc', script, file=f)
#                     print('re', region, file=f)
#                     print('ui', uid, file=f)
#                     print('gr', grp, file=f)


    #--  Dictionaries  ---------------------

    def create_dicts_tab (self):
        tab = self.load_dictionary_table()
        self.write_dicts_tab(tab)

    def load_dictionary_table (self):
        tab = {}
        for d in self.dictionaries():
            tab[d.id] = d
        return tab

    def dictionaries (self):
        with self.topen('source') as f:
            rdr = csv.reader(f)
            next(rdr)
            for r in rdr:
                d = Dictionary()
                d.id = r[0]
                d.reg_date = r[1]
                d.label = r[2]
                d.url = r[3]
                d.isbn = r[4]
                d.author = r[5]
                d.title = r[6]
                d.publisher = r[7]
                d.year = r[8]
                d.quality = r[9]
                d.grp = r[10]
                d.note = r[11]
                d.license = r[12]
                d.ip_claim = r[13]
                d.ip_claimant = r[14]
                d.ip_claimant_email = r[15]
                yield d

    def write_dicts_tab (self, dtab):
        tgtdir = self.require_target_dir()
        with open(join(tgtdir, 'dicts.tab'), 'w') as f:
            for d in self.dictionaries():
                f.write(d.id)
                f.write('\t')
                f.write(d.reg_date)
                f.write('\t')
                f.write(d.label)
                f.write('\t')
                f.write(d.url)
                f.write('\t')
                f.write(d.isbn)
                f.write('\t')
                f.write(d.author)
                f.write('\t')
                f.write(d.title)
                f.write('\t')
                f.write(d.publisher)
                f.write('\t')
                f.write(d.year)
                f.write('\t')
                f.write(d.quality)
                f.write('\t')
                f.write(d.grp)
                f.write('\t')
                f.write(d.note)
                f.write('\t')
                f.write(d.license)
                f.write('\t')
                f.write(d.ip_claim)
                f.write('\t')
                f.write(d.ip_claimant)
                f.write('\t')
                f.write(d.ip_claimant_email)
                f.write('\n')

    def create_bilex (self, tgt_lvid, gls_lvid):
        BilexInstaller(self, (tgt_lvid, gls_lvid)).run()
# IDs (all are digit strings):
#     lvid - language variety
#     mid  - meaning
#     xid  - expression
#
# Instances
#     variety


class OLD_Installer (object):

    zipfn = None # expanduser(config.get('data.panlex.zipfn'))
    dirname = None # config.get('data.panlex.dirname')
    tgtdir = None # expanduser(config.get('data.panlex.tgtdir'))

    def __init__ (self):
        if not self.zipfn:
            raise Exception("Configuration key not set: 'data.panlex.zipfn'")
        if not self.dirname:
            raise Exception("Configuration key not set: 'data.panlex.dirname'")
        if not self.tgtdir:
            raise Exception("Configuration key not set: 'data.panlex.tgtdir'")

        self._installed = None

    # stage dir is cwd/dirname
    def require_stage_dir (self):
        if not exists(self.dirname):
            zf = ZipFile(expanduser(self.zipfn))
            print('Creating', self.dirname)
            zf.extractall()
    
    def require_target_dir (self):
        if not exists(self.tgtdir):
            print('Creating', self.tgtdir)
            makedirs(self.tgtdir)
        return self.tgtdir

    def topen (self, name):
        self.require_stage_dir()
        return open(join(self.dirname, name + '.csv'))

    def print_header (self, name):
        with self.topen(name) as f:
            print(next(csv.reader(f)))

    def installed (self):
        if self._installed is None:
            self._installed = Panlex()
        return self._installed

    def require_lvtab (self):
        if not exists(join(self.tgtdir, 'varieties.tab')):
            self.create_varieties_tab()
        return self.installed().lvtab()

    def create_varieties_tab (self):
        VarietiesInstaller(self).run()
    
    def create_dicts_tab (self):
        tab = self.load_dictionary_table()
        self.write_dicts_tab(tab)

    def load_dictionary_table (self):
        tab = {}
        for d in self.dictionaries():
            tab[d.id] = d
        return tab

    def dictionaries (self):
        with self.topen('source') as f:
            rdr = csv.reader(f)
            next(rdr)
            for r in rdr:
                d = Dictionary()
                d.id = r[0]
                d.reg_date = r[1]
                d.label = r[2]
                d.url = r[3]
                d.isbn = r[4]
                d.author = r[5]
                d.title = r[6]
                d.publisher = r[7]
                d.year = r[8]
                d.quality = r[9]
                d.grp = r[10]
                d.note = r[11]
                d.license = r[12]
                d.ip_claim = r[13]
                d.ip_claimant = r[14]
                d.ip_claimant_email = r[15]
                yield d

    def write_dicts_tab (self, dtab):
        tgtdir = self.require_target_dir()
        with open(join(tgtdir, 'dicts.tab'), 'w') as f:
            for d in self.dictionaries():
                f.write(d.id)
                f.write('\t')
                f.write(d.reg_date)
                f.write('\t')
                f.write(d.label)
                f.write('\t')
                f.write(d.url)
                f.write('\t')
                f.write(d.isbn)
                f.write('\t')
                f.write(d.author)
                f.write('\t')
                f.write(d.title)
                f.write('\t')
                f.write(d.publisher)
                f.write('\t')
                f.write(d.year)
                f.write('\t')
                f.write(d.quality)
                f.write('\t')
                f.write(d.grp)
                f.write('\t')
                f.write(d.note)
                f.write('\t')
                f.write(d.license)
                f.write('\t')
                f.write(d.ip_claim)
                f.write('\t')
                f.write(d.ip_claimant)
                f.write('\t')
                f.write(d.ip_claimant_email)
                f.write('\n')

    def create_bilex (self, tgt_lvid, gls_lvid):
        BilexInstaller(self, (tgt_lvid, gls_lvid)).run()

class Collector (object):

    def __init__ (self, installer, flatten=True):
        self.installer = installer
        self.flatten = flatten
        self.state = 0

        # mid -> [xid,...]
        self.mtab = {}

        # if flatten=True:  xid -> str
        # else:             xid -> (lvid, str)
        self.xtab = {}

    def __enter__ (self):
        return self

    def add_mid (self, mid):
        assert self.state == 0
        self.mtab[mid] = []

    def add_xid (self, xid):
        assert self.state == 0
        self.xtab[xid] = None

    def _create_mtab (self):
        print('Create mtab')
        tab = self.mtab
        with self.installer.topen('denotation') as f:
            rdr = csv.reader(f)
            next(rdr)
            for r in rdr:
                (_, mid, xid) = r
                if mid in tab:
                    tab[mid].append(xid)
        for lst in tab.values():
            for xid in lst:
                self.add_xid(xid)

    def _create_xtab (self):
        print('Create xtab')
        tab = self.xtab
        with self.installer.topen('expr') as f:
            rdr = csv.reader(f)
            next(rdr)
            for r in rdr:
                (xid, lvid, text, _) = r
                if xid in tab:
                    if self.flatten:
                        tab[xid] = '%05d:%s' % (int(lvid), text)
                    else:
                        tab[xid] = (lvid, text)

    def __exit__ (self, t, v, tb):
        if not t:
            self._create_mtab()
            self._create_xtab()
            self.state = 1



class VarietiesInstaller (object):

    def __init__ (self, installer):

        self.installer = installer
        self.collector = Collector(installer, flatten=True)

        # lvid -> variety
        self.lvtab = None

        # lvid -> [sid,...]
        self.stab = None
    
    def topen (self, name):
        return self.installer.topen(name)

    def open (self, name, mode='r'):
        tgtdir = self.installer.require_target_dir()
        return open(join(tgtdir, name), mode)

    def run (self):
        self._create_lvtab()
        with self.collector as c:
            for lv in self.lvtab.values():
                c.add_mid(lv.names)
                c.add_xid(lv.name)
                c.add_xid(lv.script)
                c.add_xid(lv.region)
                c.add_xid(lv.uid)

        self._create_stab()
        self._fix_varieties()
        self._check_varieties()
        self._write_varieties()

    def _create_lvtab (self):
        print('Create lvtab')
        self.lvtab = tab = {}
        with self.topen('langvar') as fin:
            rdr = csv.reader(fin)
            next(rdr)
            for r in rdr:
                lv = Variety()
                (lv.id, lv.lang_code, lv.var_code, lv.mutable, lv.name, lv.script,
                 lv.names, lv.region, lv.uid, lv.grp) = r
                tab[lv.id] = lv

    def _create_stab (self):
        print('Create lv-source table')
        self.stab = tab = {}
        with self.topen('source_langvar') as f:
            rdr = csv.reader(f)
            next(rdr)
            for r in rdr:
                (sid, lvid) = r
                if lvid in tab:
                    tab[lvid].append(sid)
                else:
                    tab[lvid] = [sid]
    
    def _fix_varieties (self):
        print('Fix varieties')
        lvtab = self.lvtab
        mtab = self.collector.mtab
        xtab = self.collector.xtab
        stab = self.stab

        for lv in self.lvtab.values():
            lv.name = xtab[lv.name]
            lv.script = xtab[lv.script]
            lv.region = xtab[lv.region]
            uid = xtab[lv.uid]
            if expr_lvid(uid) != '07257':
                print('** Bad UID expr:', uid)
            lv.uid = expr_str(uid)
            lv.names = [xtab[xid] for xid in mtab[lv.names]]
            if lv.id in stab:
                lv.dicts = stab[lv.id]
            else:
                lv.dicts = []
    
    def _check_varieties (self):
        print('Check varieties')
        for lv in self.lvtab.values():
            if lv.lang_code != lv.uid[:3]:
                print('** bad lang_code', lv.lang_code, 'uid=', lv.uid)
            if int(lv.var_code) != int(lv.uid[4:7]):
                print('** bad var_code', lv.var_code, 'uid=', lv.uid)
    
    def _write_varieties (self):
        print('Write varieties')
        with self.open('varieties.tab', 'w') as f:
            for lv in self.lvtab.values():
                f.write(lv.id)
                f.write('\t')
                f.write(lv.lang_code)
                f.write('\t')
                f.write(lv.var_code)
                f.write('\t')
                f.write(lv.mutable)
                f.write('\t')
                f.write(lv.name)
                f.write('\t')
                f.write(lv.script)
                f.write('\t')
                for name in lv.names:
                    # empty field is end of list
                    if name:
                        f.write(name)
                        f.write('\t')
                f.write('\t')
                f.write(lv.region)
                f.write('\t')
                f.write(lv.uid)
                f.write('\t')
                f.write(lv.grp)
                f.write('\t')
                f.write(' '.join(lv.dicts))
                f.write('\n')


class BilexInstaller (object):

    def __init__ (self, installer, bilang):
        self.installer = installer
        self.bilang = bilang
        self.collector = Collector(installer, flatten=False)

        # mid -> sid
        self.mstab = None

        # (tgt_str, gls_str) -> [sid,...]
        self.bilex = None

    def run (self):
        lvtab = self.installer.require_lvtab()
        lvid = self.bilang[0]
        sids = set(lvtab[lvid].dicts)

        self.create_mstab(sids)    # mid -> sid

        with self.collector as c:
            for mid in self.mstab.keys():
                c.add_mid(mid)

        self.create_bilex()
        self.write_bilex()
        
    # returns table: mid -> sid, restricted to the given sids
    def create_mstab (self, sids):
        print('Create mstab')
        self.mstab = tab = {}
        with self.installer.topen('meaning') as f:
            rdr = csv.reader(f)
            next(rdr)
            for r in rdr:
                (mid, sid) = r
                if sid in sids:
                    if mid in tab:
                        print('** Duplicate meaning ID:', mid)
                    else:
                        tab[mid] = sid

    # given xids for a meaning, choose a pair of strings based on tgt_lvid, gls_lvid
    def bilex_entries (self, xids):
        (tgt_lvid, gls_lvid) = self.bilang
        tgt_strs = []
        gls_strs = []
        xtab = self.collector.xtab
        for xid in xids:
            (lvid, s) = xtab[xid]
            if lvid == tgt_lvid:
                tgt_strs.append(s)
            elif lvid == gls_lvid:
                gls_strs.append(s)
        for tgt_str in tgt_strs:
            for gls_str in gls_strs:
                yield (tgt_str, gls_str)
    
    # returns table: (tgt_str, gls_str) -> [SID,...] 
    def create_bilex (self):
        print('Create bilex')
        mstab = self.mstab
        mtab = self.collector.mtab
        self.bilex = tab = {}
        for (mid, xids) in mtab.items():
            sid = mstab[mid]
            for key in self.bilex_entries(xids):
                if key in tab:
                    tab[key].append(sid)
                else:
                    tab[key] = [sid]
        
    def write_bilex (self):
        tgtdir = self.installer.require_target_dir()
        fn = join(tgtdir, 'bilex-' + '-'.join(self.bilang) + '.tab')
        print('Writing', fn)
        with open(fn, 'w') as f:
            for (key, sids) in self.bilex.items():
                (tgtstr, glsstr) = key
                f.write(tgtstr)
                f.write('\t')
                f.write(glsstr)
                f.write('\t')
                f.write(' '.join(sids))
                f.write('\n')
