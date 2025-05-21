from bs4 import BeautifulSoup
import requests

url = 'https://infostrefa.com/infostrefa/pl/spolki'
stock_list = []

response = requests.get(url)
soup = BeautifulSoup(response.text, features='html.parser')

table = soup.find('table', attrs={'class': 'table table-text table-text-left custom-border'})


for stock_info in soup.find_all('tr'):
    symbol = stock_info.find_all('td')[2].get_text()
    if len(symbol) == 3:
        stock_list.append(symbol)

print(stock_list)


# returns:
# ['01C', '11B', '3RG', '4MS', '4MB', '7FT', '7LV', 'ABE', 'ABK', 'AIN', 'ACG', 'ACA', 'ACT',
# 'ADX', 'ADV', 'GPH', 'AVE', 'AFH', 'ARI', 'AGO', 'AGL', 'AGP', 'AGT', 'ALL', 'AWM', 'AIT',
# 'AFC', 'ALR', 'ALG', 'ALE', 'AAT', 'ALI', 'AML', 'AMB', 'AMC', 'APL', 'EAT', 'AOL', 'ANR',
# 'APA', 'APT', 'ASA', 'APN', 'PRO', 'APC', 'APE', 'AQT', 'AQU', 'AQA', 'ARH', 'ATC', 'ARE',
# 'ARG', 'ARR', 'ART', 'AAS', 'ASB', 'ASM', 'AMV', 'ABS', 'ACP', 'ASE', 'AST', 'ASR', '1AT',
# 'ATA', 'ATD', 'ATP', 'ATS', 'ATG', 'ATJ', 'ATO', 'ATR', 'APR', 'APS', 'AUX', 'AZC', 'BKD',
# 'WIS', 'BLT', 'SAN', 'BHW', 'MIL', 'PEO', 'BBD', 'BEE', 'BFT', 'BRH', 'BRG', 'BST', 'BCM',
# 'BCS', 'BHX', 'BIP', 'BCX', 'BFC', 'BGD', 'BEP', 'BMX', 'BML', 'BIO', 'BTK', 'BPC', 'BPN',
# 'BRP', 'BLO', 'BTG', 'YOL', 'BNP', 'BBT', 'BRS', 'BOS', 'BOW', 'B24', 'BSA', 'BRA', 'BER',
# 'BSH', 'BAH', 'BRO', 'BTC', 'BDX', 'BMC', 'BVT', 'CBD', 'CPG', 'CPA', 'GBK', 'CTX', 'ELM',
# 'CRB', 'CAI', 'CRC', 'CSR', 'CAV', 'CCC', 'CCS', 'CDR', 'CDA', 'CDL', 'CLN', 'CFS', 'CTF',
# 'CRP', 'CEZ', 'CFI', 'CHP', 'CIG', 'CIE', 'CTS', 'CCE', 'CLD', 'CMI', 'CLE', 'CDT', 'COG',
# 'CLC', 'CMR', 'CMC', 'CMP', 'CPL', 'CPR', 'CLA', 'CCR', 'CRS', 'COS', 'CPD', 'OPG', 'CFG',
# 'CRJ', 'CRI', 'CPS', 'CZT', 'DAD', 'DNS', 'DAT', 'DBE', 'DCR', 'DEK', 'DKR', 'DEL', 'DEG',
# 'DVL', 'DEV', 'DBC', 'DGA', 'DGN', 'DIG', 'NFP', 'DTR', 'DNP', 'DTX', 'DOK', 'DOM', 'DOW',
# 'DRF', 'DRG', 'DGE', 'DDI', 'DPL', 'DUA', 'ECL', 'ECC', 'ECH', 'ECT', 'EDI', 'EDN', 'EFK',
# 'EKS', 'EEE', 'EEX', 'EBX', 'EKE', 'EPR', 'EGH', 'BDZ', 'ELT', 'EMA', 'EKP', 'ELQ', 'ELZ',
# 'EMC', 'EMP', 'EMU', 'ENA', 'EST', 'ENE', 'ENG', 'ENP', 'ENI', 'ENT', 'EON', 'ERA', 'ERB',
# 'ERG', 'ESG', 'ESK', 'EAH', 'EUC', 'EUR', 'EHG', 'VIV', 'EFE', 'ECK', 'ETX', 'ETL', 'EXA',
# 'EXC', 'EXM', 'FKD', 'FLG', 'FSG', 'FFI', 'FEE', 'FEM', 'FRO', 'FER', 'FIG', 'FTH', 'FON',
# 'FTL', 'BTX', 'FOR', 'FPO', 'FTE', 'FVE', 'FRW', 'FHD', 'GAL', 'GDC', 'GMB', 'GOP', 'GIF',
# 'GMV', 'GAR', 'GNG', 'GEN', 'GMT', 'GX1', 'GTP', 'GTS', 'GTN', 'GIG', 'GKI', 'GKS', 'GLC',
# 'GHY', 'GTF', 'GOB', 'GOL', 'GOV', 'VIN', 'GPW', 'GRX', 'GME', 'GRM', 'GEA', 'GRN', 'ATT',
# 'HRC', 'KTY', 'GMZ', 'GPP', 'GRC', 'GTY', 'GTC', 'HRP', 'HEL', 'HMP', 'HRS', 'HPM', 'HMI',
# 'HLD', 'HRL', 'HOR', 'HUB', 'HRT', 'HUG', 'HYD', 'HPS', 'HDR', 'IBC', 'ICG', 'ICD', 'IDH',
# 'IDM', 'IFI', 'IGT', 'IPW', 'IMC', 'IMG', 'IIA', 'IMP', 'IMS', 'INC', 'ICA', 'IVO', 'INS',
# 'IDG', 'IFA', 'ING', 'KPI', 'IGN', 'INP', 'INK', 'CAR', 'IRL', 'ITB', 'IMR', 'IUS', 'INT',
# 'IPO', 'INL', 'INM', 'IVE', 'IFC', 'IFR', 'IPE', 'IWS', 'IZB', 'IZO', 'IZS', 'JSW', 'JRH',
# 'JRC', 'JJB', 'JWW', 'K2H', 'KME', 'KBJ', 'KCI', 'KDM', 'KER', 'KGH', 'KGL', 'KPL', 'KBT',
# 'KLN', 'KGN', 'KMP', 'KOM', 'K2P', 'KOR', 'KPD', 'KCH', 'KRI', 'KRK', 'KRU', 'KVT', 'KSG',
# 'KUB', 'KPC', 'LAB', 'LCN', 'LRK', 'LRQ', 'LPS', 'LEG', 'LEN', 'LTX', 'LES', 'LET', 'LBT',
# 'LMG', 'LVC', 'LGT', 'LBD', 'LKD', 'LTM', 'LPP', 'LSI', 'LBW', 'LUD', 'LUG', 'LUK', 'LWB',
# 'MFD', 'MWT', 'M4B', 'MAB', 'MAD', 'MMS', '06N', 'MAK', 'MLB', 'MGT', 'MAN', 'MBW', 'MRK',
# 'MVP', 'MSM', 'MXC', 'MAX', 'MXP', 'MBK', 'MBF', 'MCI', 'MDI', 'MDA', 'MRD', 'MDP', 'MDG',
# 'MDB', 'ICE', 'MPS', 'MEG', 'MNC', 'MNS', 'MER', 'MRC', 'MCR', 'MEI', 'MRG', 'MET', 'MEX',
# 'MFO', 'MMD', 'MLM', 'MLK', 'MLP', 'MTN', 'MND', 'MTE', 'MIR', 'MRB', 'MLS', 'MLG', 'MMC',
# 'MBR', 'MOJ', 'MOL', 'MOC', 'MO2', 'MON', 'MLT', 'MSP', 'MSW', 'MSZ', 'MOV', 'MVR', 'MPY',
# 'VER', 'MRH', 'MZA', 'GRE', 'MCD', 'NNG', 'YAN', 'NST', 'NTW', 'NEU', 'NRS', 'NTC', 'NTV',
# 'NWG', 'NXG', 'NXB', 'NGG', 'IBS', 'NCL', 'NOB', 'NTS', 'NTU', 'NVG', 'NOV', 'NVT', 'PRI',
# 'NTT', 'NWA', '08N', 'ODL', 'OEX', 'OLY', 'OND', 'OML', 'FMG', 'ONE', 'O2T', 'ONO', 'ONC',
# 'OPN', 'OPM', 'OPI', 'OPL', 'ORG', 'OBL', 'ORL', 'OTS', 'OUT', 'OVI', 'OVO', 'OXY', 'OZE',
# 'NVA', 'PMP', 'PTE', 'PRN', 'PAS', 'PAT', 'PBG', 'PBF', 'PCG', 'PCX', 'PCR', 'PCF', 'PBX',
# 'PCO', 'PPS', 'PGE', 'PGV', 'PHR', 'PHN', 'PEN', 'PIX', 'PJP', 'PKN', 'PKO', 'PKP', 'PLG',
# 'P2B', 'PNW', 'PSM', 'PLI', 'P2C', 'PLW', 'PLZ', 'PGM', 'PNT', 'PIT', 'PEP', 'PCE', 'PXM',
# 'SFK', 'PLM', 'PTG', 'PTN', 'PWX', 'PSH', 'PFG', 'PBB', 'P24', 'PMA', 'PBT', 'PTH', 'PFM',
# 'PRM', 'PGI', 'PRT', 'PRS', 'PTW', 'ZAP', 'PPG', 'PUR', 'PDG', 'CRM', 'PZU', 'QNT', 'QRT',
# 'QON', 'QUB', 'QRS', 'R22', 'RAE', 'RFK', 'RAF', 'RBW', 'RNK', 'RWL', 'RDG', 'RCM', 'RDS',
# 'RDN', 'REG', 'RHD', 'RNC', 'RLP', 'RMK', 'REM', 'RSP', 'RND', 'RES', 'RST', 'RBS', 'RGL',
# 'RCA', 'RRH', 'ROV', 'RCW', 'RVU', 'S4E', 'SGR', 'SKN', 'SNK', 'SPL', 'SNW', 'STS', 'SLT',
# 'SCP', 'SDS', 'SWG', 'SED', 'SEK', 'SEL', 'SLV', 'SEN', 'SES', 'SEV', 'SFD', 'SFN', 'SFS',
# 'SHY', 'SHO', 'SFG', 'SIM', 'SMT', 'SKH', 'SWT', 'SKL', 'SLZ', 'SBE', 'SHD', 'SOL', 'SIN',
# 'SON', 'SOK', 'SPH', 'SPK', 'SPR', 'STX', 'STP', 'STF', 'STD', 'SHG', 'STA', 'SCS', 'STI',
# 'STH', 'SUL', 'SDG', 'SNX', 'SUN', 'SUW', 'SYG', 'SGN', 'SNT', 'SNG', 'SZR', 'SKA', 'TLX',
# 'TOS', 'TAR', 'TMR', 'TPE', 'TXN', 'TBL', 'TMP', 'TLO', 'TLS', 'TLG', 'TEN', 'THG', 'T2P',
# 'TME', 'TRR', 'TSG', 'THD', 'F51', 'TIM', 'TOR', 'TOW', 'TOA', 'TRK', 'TRN', 'TGG', 'TRI',
# 'TGS', 'UFG', 'ULM', 'ULG', 'UNF', 'UNI', 'UCG', 'UFC', 'U2K', 'UNT', 'UNL', 'UNV', 'URT',
# 'VKT', 'VAR', 'VEE', 'AER', 'VRB', 'VRC', 'VIA', 'VDS', 'VGO', 'VTL', 'VVD', 'VLT', 'VOT',
# 'VOX', 'VRF', 'VRG', 'WXF', 'WAS', 'WAT', 'WWL', 'WHH', 'WRE', 'WLT', 'WRL', 'WIK', 'WTN',
# 'WOD', 'WOJ', 'WPR', 'WPL', 'XBS', 'XPL', 'XTB', 'XTP', 'YBS', 'YTF', 'YOS', 'ZMT', 'ZEP',
# 'ZEN', 'RPC', 'ZRX', 'OTM', 'ZRE', 'ZUE', 'ZUK']
