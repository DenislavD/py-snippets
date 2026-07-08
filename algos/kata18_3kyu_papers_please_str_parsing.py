# 3kyu papers
from collections import defaultdict
from datetime import datetime

class Inspector:
    COUNTRIES = ['Arstotzka', 'Antegria', 'Impor', 'Kolechia', 'Obristan', 
        'Republia', 'United Federation']

    def __init__(self):
        self.allowed_countries = {'Arstotzka'}
        self.reqdocs = defaultdict(set) # 'country': {'access permit'}, 'workers': {'work pass'},
        self.vaxx = defaultdict(set) # 'country': {'polio', 'tetanus'}
        self.wanted = ''

    def __repr__(self):
        return (f'Inspector with allowed countries: {self.allowed_countries}, \n'
            f'required docs: {self.reqdocs.items()}, \n'
            f'required vaccinations: {self.vaxx.items()}'
            f'\n, and wanted criminal: {self.wanted}')

    def receive_bulletin(self, bulletin: str):
        print(bulletin)
        self.wanted = ''

        items = bulletin.split('\n')
        for item in items:
            #print('ITEM:', item)

            # country list
            if item.find('Allow ') == 0:
                text = item.replace('Allow ', '')
                self.allowed_countries = self.allowed_countries | set(self._get_origins(text))
                #print(f'Allowed {self._get_origins(text)}')
            if item.find('Deny ') == 0:
                text = item.replace('Deny ', '')
                self.allowed_countries = self.allowed_countries - set(self._get_origins(text))
                #print(f'Denied {self._get_origins(text)}')

            # required items
            obj = self.reqdocs
            if 'vaccination' in item:
                obj = self.vaxx
                item = item.replace(' vaccination', '')
            if 'require' in item:
                self._update_requirements(obj, item)

            if 'Wanted by the State: ' in item:
                self.wanted = item.replace('Wanted by the State: ', '')

        print(self)


    def _get_origins(self, text) -> list:
        match text.split()[0].lower():
            case 'entrants':
                return self.COUNTRIES
            case 'foreigners':
                return self.COUNTRIES[1:]
            case 'citizens':
                return text.split(' of ')[1].split(', ')
            case 'workers':
                return ['workers']


    def _update_requirements(self, obj, item): # obj = self.reqdocs or self.vaxx
        if 'no longer require' in item:
            origins, name = item.split(' no longer require ')
            origins = self._get_origins(origins)
            for key in origins:
                obj[key].discard(name.replace(' ', '_'))
            #print(f'Removed {name} for {origins}')
        else:
            origins, name = item.split(' require ')
            origins = self._get_origins(origins)
            for key in origins:
                obj[key].add(name.replace(' ', '_'))
            #print(f'Added {name} for {origins}')


    def inspect(self, docset):
        today = datetime(1982, 11, 22)
        expired_doc = False

        # parse docs
        entrant_data = defaultdict(set)
        for document, details in docset.items():
            info = details.split('\n')
            for row in info:
                if 'ID#: ' in row:
                    entrant_data['ID number'].add(row.replace('ID#: ', '').strip())
                elif 'NATION: ' in row:
                    entrant_data['nationality'].add(row.replace('NATION: ', '').strip())
                elif 'DOB: ' in row:
                    entrant_data['date of birth'].add(row.replace('DOB: ', '').strip())
                elif 'EXP: ' in row:
                    d = row.replace('EXP: ', '').strip().replace('.', '-') # ~ '1983-07-10'
                    expiration_date = datetime.fromisoformat(d)
                    if expiration_date <= today:
                        expired_doc = document
                elif 'NAME: ' in row:
                    names = row.replace('NAME: ', '').strip().split(', ', 1)
                    if self.wanted == names[1] + ' ' + names[0]:
                        return self.reply(2, )
                    entrant_data['name'].add(row.replace('NAME: ', '').strip())
                elif ': ' in row:
                    key, value = row.strip().split(': ', 1)
                    entrant_data[key.lower()].add(value)
        print(docset.items())
        print(entrant_data)
        # checks
        for key in entrant_data: # data mismatch accross docs
            if len(entrant_data[key]) > 1:
                return self.reply(2, key)

        if expired_doc:
            return self.reply(1, f'{expired_doc} expired')

        nation = entrant_data.setdefault('nationality', {'Arstotzka'}).pop()
        if nation not in self.allowed_countries:
            return self.reply(1, f'citizen of banned nation')
        
        missing_docs = self.reqdocs[nation] - set(docset)
        print(f'{missing_docs=}')
        if missing_docs:
            if 'access_permit' in missing_docs:
                if 'grant_of_asylum' in docset:
                    pass
                elif 'diplomatic_authorization' in docset:
                    if 'Arstotzka' in docset['diplomatic_authorization']:
                        print('access_permit waived:', docset.keys())
                        pass
                    else:
                        return self.reply(1, f'invalid diplomatic_authorization')
                else:
                    return self.reply(1, f'missing required {missing_docs.pop()}')
            else:
                return self.reply(1, f'missing required {missing_docs.pop()}')

        if 'access_permit' in docset:
            for row in docset['access_permit'].split('\n'):
                if 'PURPOSE: ' in row and 'WORK' in row:
                    if missing_worker_docs := self.reqdocs['workers'] - set(docset):
                        return self.reply(1, f'missing required {missing_worker_docs.pop()}')

        vaccines = entrant_data.get('vaccines')
        if vaccines:
            vaccines = vaccines.pop()
        for vax in list(self.vaxx[nation]):
            if 'certificate_of_vaccination' in self.reqdocs[nation]:
                if 'certificate_of_vaccination' not in docset:
                    return self.reply(1, f'missing required certificate_of_vaccination')
                if vax not in docset['certificate_of_vaccination']:
                    print(f'{vax} missing in certificate')
                    return self.reply(1, f'missing required vaccination')
            else:
                if not vaccines or vax.replace('_', ' ') not in vaccines:
                    print(f'{vax} missing')
                    return self.reply(1, f'missing required vaccination')

        return self.reply(0, nation)


    def reply(self, code, info=None):
        if info: info = info.replace('_', ' ')
        match code:
            case 0 if info == 'Arstotzka':
                return 'Glory to Arstotzka.'
            case 0:
                return 'Cause no trouble.'
            case 1:
                return f'Entry denied: {info}.'
            case 2 if not info:
                return f'Detainment: Entrant is a wanted criminal.'
            case 2:
                return f'Detainment: {info} mismatch.'


# tests

inspector = Inspector()
bulletin = """Entrants require passport
Foreigners require access permit
Citizens of Arstotzka require ID card
Workers require work pass
Allow citizens of Arstotzka, Obristan, test
Deny citizens of test
Entrants no longer require tetanus vaccination
Entrants require tetanus vaccination
Foreigners require polio vaccination
Citizens of Antegria no longer require polio vaccination
Wanted by the State: Hubert Popovic
"""
bulletin = """Entrants require passport
Foreigners require access permit
Allow citizens of Impor
"""
inspector.receive_bulletin(bulletin)

entrant1 = {
    "passport": """ID#: GC07D-FU8AR
    NATION: Obristan
    NAME: Guyovich, Russian
    DOB: 1933.11.28
    SEX: M
    ISS: East Grestin
    EXP: 1983.07.10""",

    "access_permit": """NAME: Guyovich, Russian
    NATION: Obristan
    ID#: GC07D-FU8AR
    PURPOSE: TRANSIT, WORK
    DURATION: 14 DAYS
    HEIGHT: 159cm
    WEIGHT: 60kg
    EXP: 1983.07.13""",

    "work_pass": """NAME: Guyovich, Russian""", 

    "certificate_of_vaccination": """ tetanus polio """, 
}

josef = {
    "passport": """ID#: GC07D-FU8AR
    NATION: Arstotzka
    NAME: Costanza, Josef
    DOB: 1933.11.28
    SEX: M
    ISS: East Grestin
    EXP: 1983.03.15"""
}
guyovich = {
    "access_permit": """NAME: Guyovich, Russian
    NATION: Obristan
    ID#: TE8M1-V3N7R
    PURPOSE: TRANSIT
    DURATION: 14 DAYS
    HEIGHT: 159cm
    WEIGHT: 60kg
    EXP: 1983.07.13"""
}
roman = {
    "passport": """ID#: WK9XA-LKM0Q
    NATION: United Federation
    NAME: Dolanski, Roman
    DOB: 1933.01.01
    SEX: M
    ISS: Shingleton
    EXP: 1983.05.12""",
    
    "grant_of_asylum": """NAME: Dolanski, Roman
    NATION: United Federation
    ID#: Y3MNC-TPWQ2
    DOB: 1933.01.01
    HEIGHT: 176cm
    WEIGHT: 71kg
    EXP: 1983.09.20"""
}

test1 = {'passport': """ID#: K8J2M-079G8
NATION: Impor
NAME: Romanoff, Patrik
DOB: 1962.09.07
SEX: M
ISS: Shingleton
EXP: 1993.02.26""", 

'diplomatic_authorization': """NAME: Romanoff, Patrik
NATION: Impor
ID#: K8J2M-079G8
ACCESS: Kolechia, Obristan, Antegria"""
}

res = inspector.inspect(test1)
print('-' * 50)
print(res)

# assert inspector.inspect(entrant1) == 'Cause no trouble.'
# assert inspector.inspect(josef) == 'Glory to Arstotzka.'
# assert inspector.inspect(guyovich) == 'Entry denied: missing required passport.'
# assert inspector.inspect(roman) == 'Detainment: ID number mismatch.'