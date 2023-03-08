# Use data from sportpesa to search through betika.com and combine all that to a csv file.
"""
Links to articles on arbitrage betting: 
    --> https://www.sbo.net/strategy/arbitrage-betting/
    --> https://thearbacademy.com/arbitrage-calculation/
"""
# import sportpesa_data
# import betika_data
import csv


# initial_data = sportpesa_data.get_sportpesa_data()
# if initial_data:
#     updated_array = betika_data.add_betika_data(initial_data)
#     for idx, item in enumerate(updated_array):
#         print(f"{idx} : {item}")
# else:
#     print("No data from the two sites")


sample_data = [
    {'teams': 'PERSIB BANDUNG vs PERSIK KEDIRI', 'start_time': '11:00',
        'event_id': 5574, 'BK': {'GG': 1.8, 'NO_GG': 1.87}},
    {'teams': 'MKE ANKARAGUCU U19 vs KAYSERISPOR U19', 'start_time': '12:00',
        'event_id': 3519, 'SP': {'GG': 1.49, 'NO_GG': 2.33}, 'BK': {'GG': 1.49, 'NO_GG': 2.33}},
    {'teams': 'GOZTEPE U19 vs FENERBAHCE U19', 'start_time': '12:00', 'event_id': 4953,
        'SP': {'GG': 1.91, 'NO_GG': 1.74}, 'BK': {'GG': 1.91, 'NO_GG': 1.74}},
    {'teams': 'PUSAMANIA BORNEO vs PERSIJA JAKARTA', 'start_time': '13:00', 'event_id': 3911,
        'SP': {'GG': 1.71, 'NO_GG': 1.94}, 'BK': {'GG': 1.76, 'NO_GG': 1.91}},
    {'teams': 'SAGAN TOSU vs CONSADOLE SAPPORO', 'start_time': '13:00', 'event_id': 5773,
        'SP': {'GG': 1.67, 'NO_GG': 1.99}, 'BK': {'GG': 1.7, 'NO_GG': 2.03}},
    {'teams': 'YOKOHAMA F MARINOS vs JUBILO IWATA', 'start_time': '13:00', 'event_id': 3288,
        'SP': {'GG': 1.7, 'NO_GG': 1.95}, 'BK': {'GG': 1.66, 'NO_GG': 2.09}},
    {'teams': 'SHIMIZU S PULSE vs KAWASAKI FRONTALE', 'start_time': '13:00',
        'event_id': 1526, 'SP': {'GG': 1.64, 'NO_GG': 2.04}, 'BK': {'GG': 1.67, 'NO_GG': 2.09}},
    {'teams': 'SHONAN BELLMARE vs URAWA RED DIAMONDS', 'start_time': '13:00',
        'event_id': 3934, 'SP': {'GG': 1.84, 'NO_GG': 1.8}, 'BK': None},
    {'teams': 'VISSEL KOBE vs NAGOYA GRAMPUS', 'start_time': '13:00', 'event_id': 2289,
        'SP': {'GG': 1.96, 'NO_GG': 1.7}, 'BK': {'GG': 2.01, 'NO_GG': 1.71}},
    {'teams': 'SANFRECCE HIROSHIMA vs YOKOHAMA', 'start_time': '13:00',
        'event_id': 5543, 'SP': {'GG': 1.9, 'NO_GG': 1.75}, 'BK': None},
    {'teams': 'KASHIWA REYSOL vs KASHIMA ANTLERS', 'start_time': '13:00', 'event_id': 5572,
        'SP': {'GG': 1.73, 'NO_GG': 1.92}, 'BK': {'GG': 1.76, 'NO_GG': 1.95}},
    {'teams': 'AVISPA FUKUOKA vs NIIGATA ALBIREX', 'start_time': '13:00', 'event_id': 4302,
        'SP': {'GG': 2.0, 'NO_GG': 1.67}, 'BK': {'GG': 2.04, 'NO_GG': 1.69}},
    {'teams': 'CEREZO OSAKA vs FC TOKYO', 'start_time': '13:00', 'event_id': 1391,
        'SP': {'GG': 1.89, 'NO_GG': 1.75}, 'BK': {'GG': 1.92, 'NO_GG': 1.79}},
    {'teams': 'KYOTO SANGA vs GAMBA OSAKA', 'start_time': '13:00', 'event_id': 3750,
        'SP': {'GG': 1.79, 'NO_GG': 1.85}, 'BK': {'GG': 1.82, 'NO_GG': 1.88}},
    {'teams': 'FC GAGRA vs DINAMO TBILISI', 'start_time': '13:30', 'event_id': 2511,
        'SP': {'GG': 2.06, 'NO_GG': 1.63}, 'BK': {'GG': 2.12, 'NO_GG': 1.61}},
    {'teams': 'GARABAGH-2 vs FK SABAYIL-2', 'start_time': '14:00',
        'event_id': 1320, 'SP': {'GG': 1.48, 'NO_GG': 2.36}, 'BK': None},
    {'teams': 'FC SAMGURALI TSKALTUBO vs FC TELAVI', 'start_time': '14:00',
        'event_id': 2537, 'SP': {'GG': 2.16, 'NO_GG': 1.57}, 'BK': {'GG': 2.2, 'NO_GG': 1.58}},
    {'teams': 'ISTANBULSPOR U 19 vs ISTANBUL BASAKSEHIR AS U19', 'start_time': '14:00',
        'event_id': 4063, 'SP': {'GG': 1.28, 'NO_GG': 3.15}, 'BK': {'GG': 1.28, 'NO_GG': 3.15}},
    {'teams': 'FC SAMTREDIA vs TORPEDO KUTAISI', 'start_time': '14:30', 'event_id': 1178,
        'SP': {'GG': 1.93, 'NO_GG': 1.72}, 'BK': {'GG': 2.0, 'NO_GG': 1.69}},
    {'teams': 'MANISA BBSK vs BODRUMSPOR', 'start_time': '14:30', 'event_id': 2616,
        'SP': {'GG': 1.74, 'NO_GG': 1.91}, 'BK': {'GG': 1.73, 'NO_GG': 1.99}},
    {'teams': 'ERZURUM BB vs KECIORENGUCU', 'start_time': '14:30',
        'event_id': 5341, 'SP': {'GG': 1.72, 'NO_GG': 1.93}, 'BK': None},
    {'teams': 'NZOIA SUGAR FC vs GOR MAHIA', 'start_time': '15:00', 'event_id': 5323,
        'SP': {'GG': 2.46, 'NO_GG': 1.44}, 'BK': {'GG': 2.44, 'NO_GG': 1.47}},
    {'teams': 'JORDAN vs OMAN', 'start_time': '15:00', 'event_id': 5424,
        'SP': {'GG': 2.5, 'NO_GG': 1.43}, 'BK': {'GG': 2.35, 'NO_GG': 1.48}},
    {'teams': 'SOUTH KOREA U20 vs TAJIKISTAN U20', 'start_time': '15:00',
        'event_id': 2094, 'SP': {'GG': 2.5, 'NO_GG': 1.43}, 'BK': None},
    {'teams': 'FC SARAJEVO vs ZELJEZNICAR', 'start_time': '15:00', 'event_id': 1513,
        'SP': {'GG': 1.9, 'NO_GG': 1.74}, 'BK': {'GG': 1.95, 'NO_GG': 1.77}},
    {'teams': 'MALISHEVA vs KF DUKAGJINI', 'start_time': '15:00', 'event_id': 3499,
        'SP': {'GG': 1.68, 'NO_GG': 1.99}, 'BK': {'GG': 1.7, 'NO_GG': 2.0}},
    {'teams': 'KF FERIZAJ vs KF LLAPI', 'start_time': '15:00', 'event_id': 4183,
        'SP': {'GG': 1.81, 'NO_GG': 1.83}, 'BK': {'GG': 1.83, 'NO_GG': 1.84}},
    {'teams': 'AYTEMIZ ALANYASPOR U19 vs GALATASARAY YOUTH', 'start_time': '15:00',
        'event_id': 4017, 'SP': {'GG': 1.56, 'NO_GG': 2.18}, 'BK': {'GG': 1.52, 'NO_GG': 2.27}},
    {'teams': 'SPVGG UNTERHACHING U19 vs MEINZ U19', 'start_time': '15:00',
        'event_id': 4376, 'SP': {'GG': 1.48, 'NO_GG': 2.36}, 'BK': None},
    {'teams': 'FC MECKLENBURG SCHWERIN vs TUS MAKKABI BERLIN', 'start_time': '15:00',
        'event_id': 5239, 'SP': {'GG': 1.49, 'NO_GG': 2.34}, 'BK': {'GG': 1.48, 'NO_GG': 2.35}},
    {'teams': 'PERAK FA vs PAHANG FA', 'start_time': '15:15', 'event_id': 1202,
        'SP': {'GG': 1.72, 'NO_GG': 1.93}, 'BK': {'GG': 1.72, 'NO_GG': 1.93}},
    {'teams': 'TSG NEUSTRELITZ vs ROSTOCKER FC', 'start_time': '15:30', 'event_id': 4707,
        'SP': {'GG': 1.53, 'NO_GG': 2.24}, 'BK': {'GG': 1.53, 'NO_GG': 2.24}},
    {'teams': 'US MONASTIR vs TP MAZEMBE', 'start_time': '16:00', 'event_id': 2336,
        'SP': {'GG': 2.09, 'NO_GG': 1.61}, 'BK': {'GG': 2.14, 'NO_GG': 1.63}},
    {'teams': 'TSHAKHUMA vs USM ALGER', 'start_time': '16:00',
        'event_id': 3030, 'SP': {'GG': 1.81, 'NO_GG': 1.83}, 'BK': None},
    {'teams': 'NK CROATIA ZMIJAVCI vs NK DUBRAVA', 'start_time': '16:00', 'event_id': 1183,
        'SP': {'GG': 1.8, 'NO_GG': 1.83}, 'BK': {'GG': 1.79, 'NO_GG': 1.89}},
    {'teams': 'FC STRUGA TRIM LUM vs SHKUPI SKOPJE', 'start_time': '16:00', 'event_id': 5725,
        'SP': {'GG': 2.18, 'NO_GG': 1.56}, 'BK': {'GG': 2.21, 'NO_GG': 1.57}},
    {'teams': 'SHKENDIJA vs RABOTNICKI SK', 'start_time': '16:00', 'event_id': 3275,
        'SP': {'GG': 2.26, 'NO_GG': 1.52}, 'BK': {'GG': 2.26, 'NO_GG': 1.54}},
    {'teams': 'SILEKS vs BREGALNICA STIP', 'start_time': '16:00', 'event_id': 1588,
        'SP': {'GG': 1.92, 'NO_GG': 1.73}, 'BK': {'GG': 1.94, 'NO_GG': 1.74}},
    {'teams': 'AKADEMIJA PANDEV vs POBEDA JUNIOR', 'start_time': '16:00',
        'event_id': 3637, 'BK': {'GG': 2.34, 'NO_GG': 1.51}},
    {'teams': 'KEDAH vs PENANG', 'start_time': '16:00', 'event_id': 1255,
        'SP': {'GG': 1.84, 'NO_GG': 1.8}, 'BK': {'GG': 1.84, 'NO_GG': 1.8}},
    {'teams': 'FK LOZNICA vs METALAC', 'start_time': '16:00', 'event_id': 2853,
        'SP': {'GG': 1.71, 'NO_GG': 1.94}, 'BK': {'GG': 1.71, 'NO_GG': 1.94}},
    {'teams': 'TABOR vs NK ROGASKA', 'start_time': '16:00', 'event_id': 3128,
        'SP': {'GG': 1.68, 'NO_GG': 1.98}, 'BK': {'GG': 1.63, 'NO_GG': 2.05}},
    {'teams': 'ETHIOPIA ELECTRICITY vs BAHIR DAR KENEMA FC', 'start_time': '16:00',
        'event_id': 4610, 'SP': {'GG': 2.18, 'NO_GG': 1.56}, 'BK': {'GG': 2.2, 'NO_GG': 1.57}},
    {'teams': 'AL ORUBAH vs AL-JABALAIN', 'start_time': '16:15', 'event_id': 5647,
        'SP': {'GG': 1.99, 'NO_GG': 1.67}, 'BK': {'GG': 2.03, 'NO_GG': 1.64}},
    {'teams': 'AC CREMA 1908 vs GIANA ERMINIO', 'start_time': '16:30', 'event_id': 4980,
        'SP': {'GG': 1.76, 'NO_GG': 1.88}, 'BK': {'GG': 1.76, 'NO_GG': 1.88}},
    {'teams': 'LIPTOVSKY MIKULAS vs MFK SKALICA', 'start_time': '16:30', 'event_id': 4033,
        'SP': {'GG': 1.65, 'NO_GG': 2.03}, 'BK': {'GG': 1.65, 'NO_GG': 2.03}},
    {'teams': 'SABURTALO TBILISI vs SHUKURA', 'start_time': '17:00',
        'event_id': 4695, 'SP': {'GG': 1.71, 'NO_GG': 1.94}, 'BK': None},
    {'teams': 'FK ARSENAL TIVAT vs BUDUCNOST', 'start_time': '17:00',
        'event_id': 5500, 'SP': {'GG': 2.2, 'NO_GG': 1.55}, 'BK': None},
    {'teams': 'JEZERO vs MORNAR BAR', 'start_time': '17:00', 'event_id': 4272,
        'SP': {'GG': 1.99, 'NO_GG': 1.68}, 'BK': {'GG': 2.05, 'NO_GG': 1.66}},
    {'teams': 'JEDINSTVO BP vs ISKRA', 'start_time': '17:00', 'event_id': 5078,
        'SP': {'GG': 1.86, 'NO_GG': 1.78}, 'BK': {'GG': 1.91, 'NO_GG': 1.76}},
    {'teams': 'RUDAR VELENJE vs MARIBOR', 'start_time': '17:00',
        'event_id': 4162, 'SP': {'GG': 2.0, 'NO_GG': 1.66}, 'BK': None},
    {'teams': 'SG DYNAMO SCHWERIN vs SC STAAKEN 1919', 'start_time': '17:00',
        'event_id': 3802, 'SP': {'GG': 1.42, 'NO_GG': 2.55}, 'BK': {'GG': 1.41, 'NO_GG': 2.55}},
    {'teams': 'KUSTOSIJA vs HNK ORIJENT 1919', 'start_time': '17:30', 'event_id': 1492,
        'SP': {'GG': 1.7, 'NO_GG': 1.95}, 'BK': {'GG': 1.75, 'NO_GG': 1.93}},
    {'teams': 'NK ALUMINIJ vs NK FUZINAR RAVNE', 'start_time': '18:00', 'event_id': 5721,
        'SP': {'GG': 1.77, 'NO_GG': 1.87}, 'BK': {'GG': 1.72, 'NO_GG': 1.93}},
    {'teams': 'BAHRAIN CLUB vs AL-SHABBAB', 'start_time': '18:30', 'event_id': 3948,
        'SP': {'GG': 2.02, 'NO_GG': 1.65}, 'BK': {'GG': 2.13, 'NO_GG': 1.61}},
    {'teams': 'AL HALA MUHARRAQ vs MANAMA CLUB', 'start_time': '18:30', 'event_id': 4629,
        'SP': {'GG': 2.11, 'NO_GG': 1.6}, 'BK': {'GG': 2.65, 'NO_GG': 1.38}},
    {'teams': 'ATROMITOS FC vs AEK ATHENS', 'start_time': '18:30', 'event_id': 4644,
        'SP': {'GG': 1.95, 'NO_GG': 1.71}, 'BK': {'GG': 2.03, 'NO_GG': 1.73}},
    {'teams': 'YOUNG AFRICANS vs AS REAL BAMAKO', 'start_time': '19:00', 'event_id': 2939,
        'SP': {'GG': 2.85, 'NO_GG': 1.34}, 'BK': {'GG': 2.9, 'NO_GG': 1.36}},
    {'teams': 'RIVERS UNITED FC vs DARING CLUB MOTEMA PEMBE', 'start_time': '19:00',
        'event_id': 3218, 'SP': {'GG': 3.05, 'NO_GG': 1.29}, 'BK': {'GG': 3.2, 'NO_GG': 1.31}},
    {'teams': 'AL AKHDAR SC vs FC SAINT ELOI LUPOPO', 'start_time': '19:00',
        'event_id': 3614, 'SP': {'GG': 2.38, 'NO_GG': 1.47}, 'BK': {'GG': 2.44, 'NO_GG': 1.49}},
    {'teams': 'ASKO vs AL ASYOOTI SPORT', 'start_time': '19:00', 'event_id': 1050,
        'SP': {'GG': 2.44, 'NO_GG': 1.45}, 'BK': {'GG': 2.5, 'NO_GG': 1.47}},
    {'teams': 'ISMAILY SC vs FARCO FC', 'start_time': '19:00', 'event_id': 3703,
        'SP': {'GG': 2.12, 'NO_GG': 1.59}, 'BK': {'GG': 2.21, 'NO_GG': 1.59}},
    {'teams': 'PARNU JK VAPRUS vs TRANS NARVA', 'start_time': '19:00', 'event_id': 3533,
        'SP': {'GG': 1.69, 'NO_GG': 1.97}, 'BK': {'GG': 1.72, 'NO_GG': 2.01}},
    {'teams': 'DILA GORI vs DINAMO BATUMI', 'start_time': '19:00', 'event_id': 3005,
        'SP': {'GG': 1.92, 'NO_GG': 1.72}, 'BK': {'GG': 1.95, 'NO_GG': 1.73}},
    {'teams': 'ADAMA CITY FC vs FASIL KENEMA', 'start_time': '19:00', 'event_id': 5601,
        'SP': {'GG': 2.19, 'NO_GG': 1.55}, 'BK': {'GG': 2.21, 'NO_GG': 1.57}},
    {'teams': 'VELEZ MOSTAR vs ZRINJSKI MOSTAR', 'start_time': '20:00', 'event_id': 3263,
        'SP': {'GG': 2.13, 'NO_GG': 1.58}, 'BK': {'GG': 2.16, 'NO_GG': 1.62}},
    {'teams': 'NOMME KALJU vs FLORA TALLINN', 'start_time': '20:00', 'event_id': 5038,
        'SP': {'GG': 1.72, 'NO_GG': 1.93}, 'BK': {'GG': 1.4, 'NO_GG': 2.6}},
    {'teams': 'LAMIA FC vs PAOK FC', 'start_time': '20:00', 'event_id': 4019,
        'SP': {'GG': 2.5, 'NO_GG': 1.42}, 'BK': {'GG': 2.41, 'NO_GG': 1.5}},
    {'teams': 'LEIKNIR vs VESTMANNAEYJAR', 'start_time': '20:00', 'event_id': 4449,
        'SP': {'GG': 1.34, 'NO_GG': 2.8}, 'BK': {'GG': 1.34, 'NO_GG': 2.85}},
    {'teams': 'PETROVAC vs RUDAR PLJEVLJA', 'start_time': '20:00', 'event_id': 4214,
        'SP': {'GG': 1.98, 'NO_GG': 1.68}, 'BK': {'GG': 2.0, 'NO_GG': 1.69}},
    {'teams': 'SUTJESKA vs DECIC TUZI', 'start_time': '20:00', 'event_id': 5583,
        'SP': {'GG': 1.99, 'NO_GG': 1.67}, 'BK': {'GG': 2.01, 'NO_GG': 1.69}},
    {'teams': 'NK NAFTA vs OLIMPIJA LJUBLJANA', 'start_time': '20:00', 'event_id': 1159,
        'SP': {'GG': 2.6, 'NO_GG': 1.4}, 'BK': {'GG': 2.5, 'NO_GG': 1.42}},
    {'teams': 'GENCLERBIRLIGI vs DENIZLISPOR', 'start_time': '20:00', 'event_id': 4313,
        'SP': {'GG': 1.74, 'NO_GG': 1.9}, 'BK': {'GG': 1.79, 'NO_GG': 1.92}},
    {'teams': 'UNION FUERSTENWALDE vs MSV PAMPOW', 'start_time': '20:00', 'event_id': 4375,
        'SP': {'GG': 1.43, 'NO_GG': 2.49}, 'BK': {'GG': 1.43, 'NO_GG': 2.5}},
    {'teams': 'VALUR REYKJAVIK W vs UMF SELFOSS W', 'start_time': '20:30',
        'event_id': 5340, 'SP': {'GG': 1.74, 'NO_GG': 1.91}, 'BK': None},
    {'teams': 'DJK GEBENBACH vs ATSV 1898 ERLANGEN', 'start_time': '20:30',
        'event_id': 3705, 'SP': {'GG': 1.4, 'NO_GG': 2.6}, 'BK': {'GG': 1.39, 'NO_GG': 2.6}},
    {'teams': 'SONDERJYSKE vs SILKEBORG IF', 'start_time': '20:45', 'event_id': 1641,
        'SP': {'GG': 1.65, 'NO_GG': 2.02}, 'BK': {'GG': 1.73, 'NO_GG': 2.0}},
    {'teams': 'WISLA PLOCK vs WARTA POZNAN', 'start_time': '20:45', 'event_id': 2284,
        'SP': {'GG': 1.79, 'NO_GG': 1.85}, 'BK': {'GG': 1.84, 'NO_GG': 1.9}},
    {'teams': 'EC SAO BERNARDO SP vs BARRETOS SP', 'start_time': '21:00',
        'event_id': 3792, 'SP': {'GG': 2.37, 'NO_GG': 1.47}, 'BK': None},
    {'teams': 'ATLETICO MINEIRO MG U20 vs AMERICA MG U20', 'start_time': '21:00',
        'event_id': 4864, 'SP': {'GG': 1.76, 'NO_GG': 1.88}, 'BK': {'GG': 1.74, 'NO_GG': 1.9}},
    {'teams': 'FORTALEZA CE U20 vs GREMIO RS U20', 'start_time': '21:00',
        'event_id': 3392, 'SP': {'GG': 1.7, 'NO_GG': 1.96}, 'BK': None},
    {'teams': 'ERFURT vs FSV LUCKENWALDE', 'start_time': '21:00', 'event_id': 5054,
        'SP': {'GG': 1.76, 'NO_GG': 1.88}, 'BK': {'GG': 1.75, 'NO_GG': 1.89}},
    {'teams': 'GUARANY DE SOBRAL vs CRATO EC CE', 'start_time': '21:30',
        'event_id': 2069, 'SP': {'GG': 2.09, 'NO_GG': 1.61}, 'BK': None},
    {'teams': 'ITAPIPOCA CE vs PACATUBA EC CE', 'start_time': '21:30', 'event_id': 3974,
        'SP': {'GG': 1.58, 'NO_GG': 2.14}, 'BK': {'GG': 1.6, 'NO_GG': 2.14}},
    {'teams': 'PAGUE MENOS CE vs ICASA CE', 'start_time': '21:30', 'event_id': 5638,
        'SP': {'GG': 1.95, 'NO_GG': 1.7}, 'BK': {'GG': 1.98, 'NO_GG': 1.71}},
    {'teams': 'FLUMINENSE EC PI vs PARNAHYBA', 'start_time': '21:45', 'event_id': 1894,
        'SP': {'GG': 2.01, 'NO_GG': 1.66}, 'BK': {'GG': 1.99, 'NO_GG': 1.71}},
    {'teams': 'DIABLES NOIRS vs ASEC MIMOSAS', 'start_time': '22:00', 'event_id': 5630,
        'SP': {'GG': 2.16, 'NO_GG': 1.57}, 'BK': {'GG': 2.19, 'NO_GG': 1.6}},
    {'teams': 'COCA COLA vs FAR RABAT', 'start_time': '22:00', 'event_id': 1114,
        'SP': {'GG': 1.77, 'NO_GG': 1.86}, 'BK': {'GG': 1.85, 'NO_GG': 1.85}},
    {'teams': 'SV AHLERSTEDT/OTTENDORF vs TUS BERSENBRUCK',
        'start_time': '22:00', 'event_id': 3286, 'BK': {'GG': 1.48, 'NO_GG': 2.35}},
    {'teams': 'CELTIC vs HEARTS', 'start_time': '22:45',
        'event_id': 5212, 'BK': {'GG': 1.87, 'NO_GG': 1.9}},
    {'teams': 'LIVINGSTON vs DUNDEE UTD', 'start_time': '22:45', 'event_id': 2820,
        'SP': {'GG': 1.81, 'NO_GG': 1.82}, 'BK': {'GG': 2.06, 'NO_GG': 1.74}},
    {'teams': 'HIBERNIAN vs RANGERS FC', 'start_time': '22:45', 'event_id': 4184,
        'SP': {'GG': 1.73, 'NO_GG': 1.91}, 'BK': {'GG': 1.94, 'NO_GG': 1.83}},
    {'teams': 'HAVANT AND WATERLOVILLE vs ST.ALBANS', 'start_time': '22:45',
        'event_id': 2444, 'SP': {'GG': 1.72, 'NO_GG': 1.93}, 'BK': None},
]

INV = 50000


def calculate_arbitrage(arr) -> list:
    """
    INFO: This function analyzes the data given and checks for arbitrage betting opportunities.
    - To calculate the arbitrage percentage, the following formula is used:
        Arbitrage % = ((1 / decimal odds for outcome A) x 100) + ((1 / decimal odds for outcome B) x 100)
    - If the result here is below 100% you have got yourself an arbitrage bet (Extremely rare stuff).

    - In case you are lucky enough:
        - Profit calculation is done as follows (Here, we use ksh 50,000):
            # Profit = Investment - ((Investment / A_odds) + (Investment / B_odds))           
        - Calculation of stake on individual outcome using the same investment amount:
            # Outcome_A_stake = Investment / A_odds, 
            # Outcome_B_stake = Investment / B_odds
    """

    count = 0
    arbs = []
    _profit = 0
    for entry in arr:
        # Get rid of entries with 'None' values
        if not "SP" in entry or not "BK" in entry or not entry["BK"]:
            arr.remove(entry)
            continue

        # Get the bigger gg values
        gg = 0
        gg_site = None
        no_gg = 0
        no_gg_site = None

        if entry["SP"]["GG"] > entry["BK"]["GG"]:
            gg = entry["SP"]["GG"]
            gg_site = "Sportpesa"
            no_gg = entry["BK"]["NO_GG"]
            no_gg_site = "Betika"
        else:
            gg = entry["BK"]["GG"]
            gg_site = "Betika"
            no_gg = entry["SP"]["NO_GG"]
            no_gg_site = "Sportpesa"

        arbitrage_percentage = round(((1/gg) * 100) + ((1/no_gg) * 100), 2)
        entry["Arb_Percentage"] = arbitrage_percentage
        if arbitrage_percentage < 100.00:
            stakes = calculate_stakes(gg, no_gg)
            entry["Stakes"] = {
                "GG": [stakes[0], gg_site],
                "NO_GG": [stakes[1], no_gg_site]
            }

            _profit = calculate_profit(gg, no_gg)
            entry["Profit"] = _profit

            arbs.append(entry)
            count += 1

    # Show output...
    print(
        f"\n Number of Arbitrage opportunities in {len(arr)} entries ---> {count} : \n")
    if arbs:
        for i in arbs:
            print(i)
            print(f"\n-----------ANALYSIS----------(Total Stake --> {INV})\n")
            print(
                f"Stake on GG ({i['Stakes']['GG'][1]}): {i['Stakes']['GG'][0]} \nStake on NO_GG ({i['Stakes']['NO_GG'][1]}): {i['Stakes']['NO_GG'][0]}")
            print(f"Profit from Ksh {INV} = Ksh {i['Profit']}")
    print("\n" * 3)

    return arr


# Profit calculation
def calculate_profit(A, B) -> float:
    profit = round(INV - ((INV / A) + (INV / B)), 2)
    return profit


# Calculating stakes
def calculate_stakes(A, B) -> list:
    A_stake = round(INV / A, 2)
    B_stake = round(INV / B, 2)
    return [A_stake, B_stake]


lst_1 = calculate_arbitrage(sample_data)


# Compiled csv report
def compiled_data(lst) -> None:
    """
    INFO: Returns a csv file with all the entries with their arbitrage percentage.
    """
    # g_header = ["Teams", "Event_id", "Start_time", "SP_GG",
    #             "SP_NO_GG", "BK_GG", "BK_NO_GG", "Arb_Percentage"]
    g_header = ["teams", "start_time",
                "event_id", "SP", "BK", "Arb_Percentage", "Profit", "Stakes"]
    # a_header = g_header + ["Total_stake", "GG_ODDS", "NO_GG_ODDS"]
    with open("all_entries.csv", "w", newline="") as f:
        g_writer = csv.DictWriter(f, fieldnames=g_header, delimiter="|")
        g_writer.writeheader()
        g_writer.writerows(lst)


compiled_data(lst_1)
