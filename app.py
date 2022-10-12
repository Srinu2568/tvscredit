import streamlit as st
import requests
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import time
import datetime as dt


# ---data for selecting in the form---
carlist = ('Maruti Wagon', 'Hyundai Creta', 'Honda Jazz', 'Maruti Ertiga', 'Audi A4', 'Nissan Micra', 'Toyota Innova', 'Volkswagen Vento', 'Tata Indica', 'Maruti Ciaz', 'Honda City', 'Maruti Swift', 'Land Rover', 'Mitsubishi Pajero', 'Honda Amaze', 'Renault Duster', 'Mercedes-Benz New', 'BMW 3', 'Audi A6', 'Hyundai i20', 'Maruti Alto', 'Toyota Corolla', 'Mahindra Ssangyong', 'Maruti Vitara', 'Mahindra KUV', 'Mercedes-Benz M-Class', 'Volkswagen Polo', 'Tata Nano', 'Hyundai Elantra', 'Hyundai Xcent', 'Hyundai Grand', 'Renault KWID', 'Hyundai i10', 'Maruti Zen', 'Ford Figo', 'Mahindra XUV500', 'Nissan Terrano', 'Honda Brio', 'Ford Fiesta', 'Hyundai Santro', 'Tata Zest', 'Maruti Ritz', 'BMW 5', 'Toyota Fortuner', 'Ford Ecosport', 'Hyundai Verna', 'Maruti Omni', 'Toyota Etios', 'Jaguar XF', 'Maruti Eeco', 'Honda Civic', 'Mercedes-Benz B', 'Mahindra Scorpio', 'Honda CR-V', 'Chevrolet Beat', 'Skoda Rapid', 'Mercedes-Benz S', 'Skoda Superb', 'Hyundai EON', 'BMW X5', 'Chevrolet Optra', 'Mercedes-Benz E-Class', 'Maruti Baleno', 'Skoda Laura', 'Skoda Fabia', 'Tata Indigo', 'Audi Q3', 'Skoda Octavia', 'Mini Cooper', 'Hyundai Santa', 'BMW X1', 'Hyundai Accent', 'Mercedes-Benz GLE', 'Maruti A-Star', 'BMW X3', 'Ford EcoSport', 'Audi Q7', 'Volkswagen Jetta', 'Mercedes-Benz GLA', 'Maruti Celerio', 'Honda Accord', 'Tata Manza', 'Chevrolet Spark', 'Maruti 800', 'Mercedes-Benz GL-Class', 'Mahindra Bolero', 'Audi Q5', 'Ford Endeavour', 'Maruti SX4', 'Toyota Camry', 'Honda Mobilio', 'Fiat Linea', 'Jeep Compass', 'Ford Ikon', 'Chevrolet Aveo', 'Mahindra Xylo', 'Nissan Sunny', 'Maruti Dzire', 'Chevrolet Cruze', 'Volkswagen Ameo', 'Mercedes-Benz CLA', 'Tata Tiago', 'BMW 7', 'Hyundai Getz', 'Hyundai Elite')
loclist = ('Mumbai', 'Pune', 'Chennai', 'Coimbatore', 'Jaipur', 'Kochi', 'Kolkata', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad')
yearlist = ('less than 2003', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022')
ownerlist = ('First', 'Second', 'Third or later')
fuellist = ('CNG', 'Diesel', 'Petrol')


# ---Data for decoding---
dctcar = {'Maruti Wagon': 67, 'Hyundai Creta': 32, 'Honda Jazz': 29, 'Maruti Ertiga': 61, 'Audi A4': 0, 'Nissan Micra': 80, 'Toyota Innova': 100, 'Volkswagen Vento': 104, 'Tata Indica': 90, 'Maruti Ciaz': 58, 'Honda City': 27, 'Maruti Swift': 65, 'Land Rover': 46, 'Mitsubishi Pajero': 79, 'Honda Amaze': 24, 'Renault Duster': 83, 'Mercedes-Benz New': 76, 'BMW 3': 5, 'Audi A6': 1, 'Hyundai i20': 43, 'Maruti Alto': 55, 'Toyota Corolla': 97, 'Mahindra Ssangyong': 50, 'Maruti Vitara': 66, 'Mahindra KUV': 48, 'Mercedes-Benz M-Class': 75, 'Volkswagen Polo': 103, 'Tata Nano': 93, 'Hyundai Elantra': 34, 'Hyundai Xcent': 41, 'Hyundai Grand': 37, 'Renault KWID': 84, 'Hyundai i10': 42, 'Maruti Zen': 68, 'Ford Figo': 21, 'Mahindra XUV500': 51, 'Nissan Terrano': 82, 'Honda Brio': 25, 'Ford Fiesta': 20, 'Hyundai Santro': 39, 'Tata Zest': 95, 'Maruti Ritz': 63, 'BMW 5': 6, 'Toyota Fortuner': 99, 'Ford Ecosport': 18, 'Hyundai Verna': 40, 'Maruti Omni': 62, 'Toyota Etios': 98, 'Jaguar XF': 44, 'Maruti Eeco': 60, 'Honda Civic': 28, 'Mercedes-Benz B': 69, 'Mahindra Scorpio': 49, 'Honda CR-V': 26, 'Chevrolet Beat': 12, 'Skoda Rapid': 88, 'Mercedes-Benz S': 77, 'Skoda Superb': 89, 'Hyundai EON': 33, 'BMW X5': 10, 'Chevrolet Optra': 14, 'Mercedes-Benz E-Class': 71, 'Maruti Baleno': 56, 'Skoda Laura': 86, 'Skoda Fabia': 85, 'Tata Indigo': 91, 'Audi Q3': 2, 'Skoda Octavia': 87, 'Mini Cooper': 78, 'Hyundai Santa': 38, 'BMW X1': 8, 'Hyundai Accent': 31, 'Mercedes-Benz GLE': 74, 'Maruti A-Star': 54, 'BMW X3': 9, 'Ford EcoSport': 17, 'Audi Q7': 4, 'Volkswagen Jetta': 102, 'Mercedes-Benz GLA': 73, 'Maruti Celerio': 57, 'Honda Accord': 23, 'Tata Manza': 92, 'Chevrolet Spark': 15, 'Maruti 800': 53, 'Mercedes-Benz GL-Class': 72, 'Mahindra Bolero': 47, 'Audi Q5': 3, 'Ford Endeavour': 19, 'Maruti SX4': 64, 'Toyota Camry': 96, 'Honda Mobilio': 30, 'Fiat Linea': 16, 'Jeep Compass': 45, 'Ford Ikon': 22, 'Chevrolet Aveo': 11, 'Mahindra Xylo': 52, 'Nissan Sunny': 81, 'Maruti Dzire': 59, 'Chevrolet Cruze': 13, 'Volkswagen Ameo': 101, 'Mercedes-Benz CLA': 70, 'Tata Tiago': 94, 'BMW 7': 7, 'Hyundai Getz': 36, 'Hyundai Elite': 35}
dctloc = {'Mumbai': 9, 'Pune': 10, 'Chennai': 2, 'Coimbatore': 3, 'Jaipur': 6, 'Kochi': 7, 'Kolkata': 8, 'Delhi': 4, 'Bangalore': 1, 'Hyderabad': 5, 'Ahmedabad': 0}
dctyear = {'2022':20,'2021':19,'2020':18,'2019':17,"2018":16,"2017":15,"2016":14,"2015":13,"2014":12,"2013":11,"2012":10,"2011":9,"2010":8,"2009":7,"2008":6,"2007":5,"2006":4,"2005":3,"2004":2,"2003":1,"less than 2003":0}
dctowner = {'First':2, 'Second':1, 'Third or later':0}
dctfuel = {'CNG':0, 'Diesel':1, 'Petrol':0}

# ----data for the bike-------
dctbike = {'TVS Star City Plus Dual Tone 110cc': 401, 'Royal Enfield Classic 350cc': 295, 'Triumph Daytona 675R': 411, 'TVS Apache RTR 180cc': 375, 'Yamaha FZ S V 2.0 150cc-Ltd. Edition': 426, 'Yamaha FZs 150cc': 437, 'Honda CB Hornet 160R  ABS DLX': 189, 'Hero Splendor Plus Self Alloy 100cc': 168, 'Royal Enfield Thunderbird X 350cc': 326, 'Royal Enfield Classic Desert Storm 500cc': 304, 'Yamaha YZF-R15 2.0 150cc': 464, 'Yamaha FZ25 250cc': 432, 'Bajaj Pulsar NS200': 72, 'Bajaj Discover 100M': 27, 'Bajaj Discover 125M': 31, 'Bajaj Pulsar NS200 ABS': 73, 'Bajaj Pulsar RS200 ABS': 76, 'Suzuki Gixxer SF 150cc': 339, 'Benelli 302R 300CC': 84, 'Hero Splendor iSmart Plus IBS 110cc': 173, 'Royal Enfield Classic Chrome 500cc': 302, 'Yamaha FZ V 2.0 150cc': 429, 'Hero Super Splendor 125cc': 176, 'Honda CBF Stunner 125cc': 214, 'Bajaj Pulsar 150cc': 56, 'Honda X-Blade 160CC ABS': 235, 'Bajaj Avenger 220cc': 9, 'KTM RC 390cc': 257, 'Honda CB Unicorn 150cc': 208, 'KTM Duke 200cc': 249, 'Honda CBR 150R 150cc': 215, 'Royal Enfield Thunderbird X 500cc': 328, 'KTM RC 200cc ABS': 256, 'Royal Enfield Thunderbird 350cc': 323, 'Royal Enfield Bullet Electra 350cc': 288, 'Bajaj Avenger Street 220 ABS': 16, 'Mahindra Centuro NXT 110cc': 277, 'Hero Hunk 150cc': 140, 'Suzuki Gixxer SF Fi 150cc SP ABS': 348, 'Yamaha FZ 150cc': 422, 'Royal Enfield\u200e Bullet 350cc': 329, 'TVS Apache RTR 160cc': 370, 'Honda CB Shine 125cc': 197, 'Benelli TNT 600i ABS': 89, 'Honda Dream Yuga 110cc': 229, 'Yamaha SZ 150cc': 449, 'Suzuki Gixxer 150cc': 333, 'Bajaj Avenger Cruise 220': 10, 'Kawasaki Z900': 272, 'Bajaj Pulsar 220cc': 65, 'Hero CD Deluxe 100cc': 122, 'Kawasaki Ninja 650cc': 264, 'Bajaj Platina 125cc': 50, 'Hero Karizma ZMR 223cc': 147, 'Bajaj Pulsar 180cc': 61, 'Yamaha FZ25 ABS 250cc': 433, 'Bajaj CT 100 100cc': 20, 'Royal Enfield Interceptor 650cc': 318, 'KTM Duke 250cc': 251, 'Royal Enfield Himalayan 410cc': 313, 'Bajaj Pulsar 135LS': 54, 'Bajaj Pulsar 220F': 64, 'Yamaha FZ16 150cc': 431, 'Ducati Scrambler 1100 Special': 102, 'Triumph Street Triple 765': 413, 'Bajaj V15 150cc': 79, 'Suzuki Gixxer Fi 150cc ABS': 338, 'Hero Splendor plus 100cc': 174, 'KTM Duke 390cc': 253, 'Honda CBR 250R': 217, 'Bajaj Pulsar RS200': 74, 'Benelli TNT 600i': 88, 'Suzuki Gixxer 150cc SP Rear Disc': 337, 'Yamaha FZ S V 2.0 150cc': 424, 'Royal Enfield Classic 500cc': 300, 'Hyosung GT650R': 242, 'Yamaha YZF-R15 S 150cc': 465, 'TVS Apache RTR 160 4V Disc': 367, 'Benelli TNT 300': 86, 'Honda CB ShineSP 125cc': 201, 'Hero Passion Pro 100cc': 151, 'Hero Splendor Plus 100cc': 165, 'Yamaha YZF R6 600cc': 461, 'Ducati 1299 Superleggera': 94, 'Royal Enfield Electra 350cc': 312, 'TVS Phoenix Disc 125cc': 394, 'Harley-Davidson Street 750': 109, 'Royal Enfield Himalayan 410cc Fi ABS': 315, 'Bajaj Discover 150cc': 40, 'Bajaj Avenger Street 220': 15, 'Royal Enfield Standard 350cc': 321, 'Honda CB Shine 125cc Disc': 199, 'Honda CB Unicorn ABS 150cc': 212, 'Yamaha YZF-R15 V3 150cc': 466, 'Bajaj Pulsar NS 200': 68, 'Bajaj Dominar 400': 43, 'Honda X-Blade 160cc': 236, 'Suzuki Hayabusa 1300cc': 349, 'Ducati Monster 821 Dark': 99, 'Yamaha FZ S V 2.0 150cc Rear Disc': 425, 'Suzuki Gixxer SF 150cc Special MOTOGP Edition Rear Disc': 344, 'KTM RC 200cc': 255, 'Bajaj Discover 125ST': 32, 'Hero Splendor Plus Kick Alloy 100cc': 167, 'Hero Karizma 223cc': 145, 'Hero Splendor 100cc': 160, 'Ducati 1198 SP 1198cc': 93, 'Royal Enfield Bullet 500cc': 287, 'Yamaha Fazer 150cc': 438, 'Yamaha Gladiator 125cc': 443, 'Hero Karizma R 223cc': 146, 'Harley-Davidson Iron 883': 106, 'TVS Apache RTR 200 4V Fi': 387, 'TVS Apache RTR 160 4V DISC ABS BS6': 365, 'Bajaj Dominar 400 ABS': 44, 'Royal Enfield Classic Gunmetal Grey 350cc': 306, 'Hero HF Deluxe i3s iBS 100cc': 135, 'Suzuki Gixxer SF Fi 150cc ABS': 347, 'Hero Splendor iSmart 110cc': 172, 'Bajaj Platina 100cc': 46, 'TVS Apache RTR 200 4V FI': 385, 'Royal Enfield Bullet Twinspark 350cc': 292, 'TVS Star City 110cc': 399, 'Bajaj Platina  Alloy ES-100cc': 45, 'Ducati Panigale 959': 101, 'Royal Enfield Classic 350cc-Redditch Edition': 298, 'TVS Sport 100cc': 396, 'Bajaj Pulsar AS200': 67, 'Royal Enfield Classic Desert Storm 500cc Dual Disc': 305, 'Honda Livo 110cc': 231, 'Suzuki Gixxer SF 150cc SP Rear Disc': 342, 'Yamaha SZ-RR 150cc': 452, 'Royal Enfield Thunderbird 500cc': 325, 'Royal Enfield Bullet Electra Twinspark 350cc': 290, 'Bajaj Discover 150F Disc': 38, 'Yamaha Saluto 125cc Disc Special Edition': 457, 'Triumph Street Triple ABS 675cc': 414, 'Honda CBR 250R ABS': 218, 'Hyosung Aquila GV250': 238, 'Jawa Forty Two 295CC': 246, 'Bajaj V12 125cc': 77, 'Bajaj V12 125cc Disc': 78, 'Yamaha Fazer 25 250cc': 439, 'Hero Xpulse 200T': 178, 'Honda CB Hornet 160R CBS': 193, 'Suzuki Gixxer 150cc SP ABS': 336, 'Hero Passion Xpro 110cc': 159, 'Yamaha YZF-R3 320cc ABS': 469, 'Royal Enfield Bullet 350 cc': 285, 'Hero HF Deluxe 100cc': 130, 'Honda CB Twister 110cc': 206, 'Bajaj Pulsar 125cc Disc CBS': 53, 'Honda CB Shine 125cc Drum BS6': 200, 'Honda CB Hornet 160R STD': 194, 'Honda Dream Neo 110cc': 228, 'BMW G 310 R': 2, 'Bajaj Pulsar AS150': 66, 'Kawasaki Ninja 250cc': 259, 'Benelli TNT 899': 90, 'Indian Chief Classic 1800cc': 244, 'Hero Achiever 150cc': 113, 'TVS Apache 150cc': 359, 'Kawasaki ER-6n 650cc': 258, 'Hero HF Deluxe Self 100cc': 132, 'Bajaj Pulsar NS160': 70, 'Royal Enfield Classic Gunmetal Grey 350cc ABS': 307, 'Suzuki Intruder 150cc': 353, 'TVS Apache RTR 200 4V ABS Race Edition': 379, 'Bajaj CT 100 B': 22, 'Hero Passion Pro 110cc Drum': 153, 'Yamaha YZF-R15 150cc': 463, 'TVS Apache RTR 160 4V DISC ABS': 364, 'Mahindra Mojo 300cc': 279, 'TVS Apache RTR 200 4V Carburetor': 380, 'Hero Ignitor Disc 125cc': 143, 'Bajaj Avenger Street 150': 12, 'Royal Enfield Continental GT 535cc': 310, 'Hero Glamour Disc 125cc': 124, 'Suzuki Gixxer SF Fi 150cc': 346, 'Hero HF Dawn 100cc': 128, 'Suzuki Slingshot Plus 125cc': 356, 'Mahindra Centuro Rockstar 110cc': 278, 'Mahindra Centuro 110cc': 276, 'Honda CB Hornet 160R Special Edition STD': 195, 'Harley-Davidson Street Rod XG750A ABS': 111, 'Hero Splendor Plus IBS i3S 100cc': 166, 'Bajaj Discover 135cc': 36, 'Bajaj Discover 125cc': 34, 'TVS Apache RTR 160 4V DRUM ABS': 366, 'Honda CB Unicorn 160 CBS': 210, 'KTM Duke 125cc': 248, 'Bajaj Boxer BM150': 18, 'Hero Glamour 125cc': 123, 'Bajaj Discover 100cc': 29, 'Bajaj Avenger Street 180': 14, 'TVS Star City Plus 110cc': 400, 'Honda CB Trigger 150cc': 205, 'Kawasaki Ninja 650 KRT Edition': 263, 'Bajaj Platina 100cc ComforTec Alloy': 47, 'Benelli TNT R 1130cc': 91, 'Honda CB Unicorn Dazzler 150cc': 213, 'Benelli TNT 600 GT': 87, 'Hyosung GT250R': 241, 'Yamaha YZF-R1 1000cc': 462, 'Hero Xtreme 200R': 181, 'Ducati Diavel 1200cc': 95, 'Triumph Speed Triple 1050cc': 412, 'Indian Scout Bobber 1130cc': 245, 'Bajaj V15 150cc POWER UP': 80, 'Jawa Standard 295CC': 247, 'Yamaha SZR 150cc': 453, 'TVS Star Sport 100cc': 402, 'Hyosung Aquila 250 250cc': 237, 'Kawasaki Z650': 270, 'Hero CD Dawn 100cc': 121, 'TVS Apache RTR 200 4V ABS': 378, 'Hero Passion 100cc': 148, 'Suzuki Intruder SP 150cc': 355, 'Yamaha YZF-R3 320cc': 468, 'TVS Apache RR310': 360, 'Hero Passion Plus 100cc': 150, 'Royal Enfield Classic 350cc-Redditch Edition Dual Disc': 299, 'Hero CBZ 150cc': 116, 'Yamaha FZS FI 150cc': 434, 'Honda CB Unicorn 160 STD': 211, 'Suzuki GS 150 R 150cc': 330, 'Royal Enfield Machismo 500cc': 320, 'Hero CBZ Xtreme 150cc': 119, 'Yamaha SZ RR V 2.0 150cc': 450, 'TVS Apache RTR 180cc ABS': 376, 'Hero Honda Splendor 100cc': 138, 'Honda CBR 150R Deluxe': 216, 'Hero Ignitor 125cc': 142, 'Bajaj Pulsar 200cc': 63, 'Kawasaki Ninja 300cc': 261, 'Kawasaki Ninja 300 ABS': 260, 'Bajaj Pulsar 150cc Rear Disc': 59, 'Hero Splendor NXG 100cc': 161, 'Hero Achiever Disc 150cc': 114, 'TVS Apache RTR 200 4V Carburetor Race Edition 2.0': 383, 'Royal Enfield Thunderbird 350cc ABS': 324, 'Harley-Davidson Street 750 ABS': 110, 'Bajaj Pulsar 150cc Rear Disc ABS': 60, 'KTM Duke 250cc ABS': 252, 'Bajaj Pulsar 200 NS 200cc': 62, 'Mahindra Mojo Tourer Edition 300cc': 280, 'Hero Passion Pro i3S Alloy 100cc': 155, 'Royal Enfield Thunderbird X 350cc ABS': 327, 'Hero Xtreme 150cc': 180, 'Bajaj Boxer CT100': 19, 'Royal Enfield Bullet 350cc': 286, 'Royal Enfield Standard 500cc': 322, 'Hyosung Aquila Pro GV650': 239, 'Royal Enfield Classic 500cc Dual Disc': 301, 'Suzuki V-Strom 1000cc': 357, 'KTM RC 125CC': 254, 'Suzuki Gixxer SF 250cc ABS': 345, 'Harley-Davidson 1200 Custom': 104, 'Honda Dream Yuga 110cc CBS': 230, 'Hero Splendor Pro 100cc': 169, 'Suzuki Hayate 110cc': 350, 'Yamaha Fazer FI V 2.0 150cc': 441, 'TVS Victor 110cc Disc': 405, 'Royal Enfield Classic Stealth Black 500cc': 309, 'TVS Apache RTR 200 4V Dual Channel ABS BS6': 384, 'Honda CB Shine 125cc CBS': 198, 'Honda Livo Disc 110cc': 232, 'Bajaj Discover 110cc': 30, 'Suzuki Gixxer SF 150cc ABS': 340, 'Hero CD 100SS': 120, 'Hero Honda Splendor Plus 100cc': 139, 'Bajaj Discover 100T': 28, 'Hero HF Deluxe self Alloy 100cc': 136, 'Benelli TNT 25 250cc': 85, 'Yamaha MT-15 150cc': 445, 'Yamaha FZS FI 150cc Rear Disc': 435, 'TVS Apache RTR 200 4V Carburetor Pirelli Tyres': 381, 'Triumph Tiger 800 XRX': 420, 'Ducati XDiavel 1262CC S': 103, 'TVS Suzuki Shogun 110cc': 403, 'Bajaj Discover 125cc Disc': 35, 'Triumph Thunderbird Storm 1700cc': 417, 'Suzuki GSX-S750': 332, 'TVS Flame 125cc': 390, 'Triumph Tiger 800 XCA': 418, 'Royal Enfield Machismo 350cc': 319, 'TVS Victor 110cc': 404, 'Honda CBR650R': 224, 'Hero Xpulse 200cc FI': 179, 'Hero HF Deluxe i3s 100cc': 134, 'TVS Apache RTR 160cc Matt Red Rear Disc': 371, 'Rajdoot GTX 175cc': 284, 'Hero Xtreme 200R ABS': 182, 'Honda CB Unicorn 160': 209, 'Honda CB Hornet 160R Special Edition-CBS': 196, 'TVS Apache RTR 200 4V Carburetor Pirelli Tyres Race Edition 2.0': 382, 'TVS Apache RR310 Slipper Clutch': 361, 'Mahindra Mojo UT300': 281, 'Royal Enfield Bullet Twinspark Kickstart 350cc': 294, 'Bajaj Pulsar  180cc': 52, 'Honda CD 110 Dream': 225, 'Royal Enfield Bullet Twinspark 500cc': 293, 'Hero Xtreme Sports Rear Disc 150cc': 185, 'Bajaj CT 100 ES Alloy': 23, 'Bajaj  Pulsar 180cc': 5, 'Bajaj Discover 150F': 37, 'Hyosung GT 650N': 240, 'Triumph Street Twin 900cc': 415, 'Bajaj CT 100 Alloy': 21, 'TVS Apache RTR 160 4V Drum': 368, 'Yamaha SZ RR V 2.0 150cc Limited Edition': 451, 'Yamaha YZF-R1M 1000cc': 467, 'Hero Glamour i3s 125cc': 127, 'Harley-Davidson Roadster XL 1200CX': 107, 'Triumph Tiger 800 XR': 419, 'KTM Duke 200cc ABS': 250, 'Honda CBR1000RR Fireblade': 223, 'Honda SP125 Disc BS6': 234, 'Bajaj Platina 110 H Gear Disc': 49, 'Hero Splendor Plus 100 cc': 164, 'Honda CBR 250R Repsol': 219, 'Triumph Bonneville T100 865cc': 408, 'Yamaha RX135 135cc 4-Speed': 447, 'Benelli 302R': 83, 'Hero Splendor iSmart 100cc': 171, 'Royal Enfield Classic 350cc Dual Disc': 296, 'Honda CB 1000R': 187, 'Honda CBR 600RR': 221, 'Ducati Monster 797': 98, 'Ducati Monster 1200': 96, 'Suzuki GSX-R 1000cc': 331, 'Ducati Monster 796 Corse Stripe': 97, 'TVS Victor 110cc Disc SBT': 406, 'Honda CB ShineSP 125cc CBS Disc': 203, 'Kawasaki Z250': 269, 'Royal Enfield Classic Squadron Blue 500cc': 308, 'Suzuki Gixxer 150cc Dual Tone Rear Disc': 335, 'TVS Apache RTR 200 4V': 377, 'Honda Livo Disc 110cc CBS': 233, 'TVS Apache RTR 160cc Rear Disc': 372, 'Yamaha FZ S V 3.0 150cc': 427, 'BMW G 310 GS': 1, 'Royal Enfield Classic 350cc Signals Edition': 297, 'Royal Enfield Bullet Electra Twinspark 350cc Double Disc': 291, 'Honda CB Hornet 160R 160cc STD': 191, 'Suzuki Intruder 150cc FI': 354, 'Bajaj Platina 110 CBS': 48, 'Hero Xtreme Sports 150cc': 184, 'Bajaj Avenger Cruise 220 ABS': 11, 'Honda CB Hornet 160R 160cc STD SP': 192, 'Kawasaki Versys 650cc': 266, 'Ducati Multistrada 1200 Enduro': 100, 'Hero Passion Pro i3S Alloy 100cc IBS': 156, 'Hero Xtreme Sports 149cc': 183, 'TVS Apache RTR 160 4V Carburetor': 362, 'Triumph Thruxton R 1200cc': 416, 'Honda CD 110 Dream DX': 226, 'BMW S 1000 XR Pro': 4, 'Honda CB ShineSP 125cc Disc': 204, 'Hero HF Deluxe Eco 100cc': 131, 'Bajaj XCD 125': 81, 'Honda CB ShineSP 125cc CBS': 202, 'Bajaj CT110 ES Alloy': 26, 'TVS Apache RTR 160 4V FI': 369, 'Triumph Bonneville T100 900cc': 409, 'Bajaj Avenger Street 160 ABS': 13, 'TVS Apache RTR 160cc White Race Edition Rear Disc': 374, 'Royal Enfield Himalayan 410cc Sleet Edition': 317, 'Hero Splendor+ 100cc': 175, 'Suzuki Gixxer SF 150cc Rear Disc': 341, 'TVS Apache RTR 160 4V Carburetor With Rear Disc': 363, 'Suzuki Heat 125cc': 352, 'Honda CB Hornet 160R  ABS STD': 190, 'Yamaha Fazer25 250cc': 442, 'Bajaj Pulsar NS160 Rear Disc': 71, 'Honda CB Hornet 160R': 188, 'Bajaj Discover150 150cc': 41, 'Bajaj Discover 125T': 33, 'Bajaj Pulsar 150cc Classic': 57, 'Yamaha Saluto 125cc': 456, 'Hero Passion XPRO 110 cc': 158, 'Yamaha FZS FI 150cc Special Edition': 436, 'TVS Fiero 150cc': 389, 'Mahindra Mojo XT300': 282, 'Bajaj Platina Alloy ES 100cc': 51, 'TVS Jive 110cc': 391, 'Bajaj Boxer AT100': 17, 'Bajaj Discover 150S Disc': 39, 'TVS Radeon 110cc Drum SBT': 395, 'Honda CD 110 Dream Self': 227, 'Suzuki Gixxer 150cc ABS': 334, 'Suzuki Hayate EP 110cc': 351, 'Yamaha SZX 150cc': 455, 'Hero CBZ Star 160cc': 117, 'Hero Passion PRO  100 cc': 149, 'Hero Passion Pro i3S Disc 100cc': 157, 'Bajaj Avenger 200cc': 8, 'Hero Honda Ambition 135cc': 137, 'Bajaj Pulsar 135LS 135cc': 55, 'Bajaj CT 100 KS Alloy': 24, 'BMW S 1000 RR Pro': 3, 'Kawasaki Versys 1000': 265, 'Honda CB Unicorn 150 150cc': 207, 'Kawasaki Z800': 271, 'Hero Glamour PGM Fi 125cc': 126, 'Royal Enfield Continental GT 650cc': 311, 'LML Freedom DX 110cc': 273, 'Harley-Davidson XG750 750cc': 112, 'Yezdi Classic 250cc': 470, 'Hero Passion Pro 100cc Drum Alloy': 152, 'TVS Star 100cc': 398, 'Bajaj XCD 135': 82, 'Bajaj Avenger 150cc': 6, 'Hero HF Deluxe 100 cc': 129, 'Yamaha Fazer FI 150cc': 440, 'TVS Apache RTR 200 4V FI Race Edition 2.0': 386, 'Yamaha FZ V 3.0 150cc': 430, 'Hero Super Splendor 125cc i3s': 177, 'Yamaha SS 125 125cc': 448, 'Suzuki Gixxer SF 150cc Special MOTOGP Edition': 343, 'TVS Victor GX 110cc': 407, 'TVS Apache RTR 200 4V Race Edition 2.0': 388, 'Hero Passion Pro TR 100cc': 154, 'Honda CBR 650 F': 222, 'Yamaha FZ S V 3.0 150cc ABS Dark Knight BS VI': 428, 'Hero HF Deluxe Self Spoke 100cc': 133, 'TVS Sports plus ES 100cc': 397, 'BMW F750 GS 850cc': 0, 'Royal Enfield Bullet Electra Twinspark 350CC ABS': 289, 'Hero Glamour Fi 125cc': 125, 'Royal Enfield Himalayan 410cc Sleet ABS': 316, 'Bajaj Pulsar NS 200cc': 69, 'Yamaha YBR 110cc': 460, 'Bajaj CT 100 Spoke': 25, 'Yamaha Crux 110cc': 421, 'Yamaha Saluto RX 110cc': 459, 'MV Agusta Brutale 1090': 274, 'Royal Enfield Himalayan 410cc Fi': 314, 'MV Agusta F3 800cc': 275, 'Kawasaki Ninja 400': 262, 'Benelli TRK 502X': 92, 'TVS Phoenix 125cc': 393, 'Harley-Davidson Fat Bob 107 Ci': 105, 'TVS Apache RTR 160cc White Race Edition': 373, 'Ideal Jawa Yezdi CL-II 250 cc': 243, 'Hero Splendor Pro Classic 100cc': 170, 'Yamaha FZ Fi Version 2.0 150cc': 423, 'Yamaha SZS 150cc': 454, 'Triumph Daytona 675 ABS': 410, 'Royal Enfield Classic Chrome 500cc ABS': 303, 'Harley-Davidson Sportster 883': 108, 'Suzuki Zeus 125cc': 358, 'Yamaha Saluto 125cc-Special Edition': 458, 'Bajaj Avenger 180cc': 7, 'Bajaj Pulsar 150cc Neon': 58, 'Kawasaki Z1000': 268, 'Hero CBZ Xtreme 150 cc': 118, 'Kawasaki Vulcan S 650cc': 267, 'Yamaha RX-Z 135cc': 446, 'Yamaha Libero G5 110cc': 444, 'Bajaj Pulsar RS200  ABS-200cc': 75, 'Bajaj Discover150S 150cc': 42, 'Hero i Smart 125cc': 186, 'Hero Splendor Plus  100 cc': 162, 'Hero Splendor Plus 100 CC': 163, 'Hero Karizma 223 cc': 144, 'TVS MAX 4R 110cc': 392, 'Mahindra Pantero 110cc': 283, 'Hero Ambition 135cc': 115, 'Honda CBR 250R Repsol ABS': 220, 'Hero Hunk Rear Disc 150cc': 141}

dctbrand = {'TVS': 19, 'Royal Enfield': 17, 'Triumph': 20, 'Yamaha': 21, 'Honda': 6, 'Hero': 5, 'Bajaj': 1, 'Suzuki': 18, 'Benelli': 2, 'KTM': 11, 'Mahindra': 15, 'Kawasaki': 12, 'Ducati': 3, 'Hyosung': 7, 'Harley-Davidson': 4, 'Jawa': 10, 'BMW': 0, 'Indian': 9, 'Rajdoot': 16, 'LML': 13, 'Yezdi': 22, 'MV': 14, 'Ideal': 8}

dctcity = {'Ahmedabad': 6, 'Delhi': 118, 'Bangalore': 44, 'Mumbai': 282, 'Kalyan': 218, 'Faridabad': 140, 'Mettur': 273, 'Hyderabad': 185, 'Kaithal': 217, 'Gurgaon': 167, 'Pune': 330, 'Noida': 308, 'Nashik': 300, 'Kochi': 240, 'Allahabad': 14, 'Samastipur': 359, 'Nadiad': 289, 'Lucknow': 257, 'Jaipur': 191, 'Karnal': 224, 'Gorakhpur': 163, 'Vidisha': 431, 'Hosur': 182, 'Bagalkot': 36, 'Baripara': 54, 'Agra': 5, 'Dharwad': 128, 'Vadodara': 423, 'Jalandhar': 194, 'Surat': 395, 'Chennai': 100, 'Navi Mumbai': 301, 'Gandhidham': 149, 'Visakhapatnam': 436, 'Thrissur': 404, 'Kolkata': 243, 'Ernakulam': 137, 'Barasat': 50, 'Ghaziabad': 156, 'Bhubaneshwar': 74, 'Amritsar': 21, 'Bhopal': 73, 'Hamirpur(hp)': 172, 'Kottayam': 248, 'Arrah': 30, 'Patiala': 321, 'Ranga Reddy': 346, 'Mandi': 262, 'Ludhiana': 258, 'Mandya': 264, 'Siliguri': 379, 'Aurangabad': 32, 'Kanpur': 220, 'Bhilwara': 69, 'Meerut': 271, 'Rewari': 352, 'Ahmednagar': 7, 'Wardha': 439, 'Chandigarh': 96, 'Ranchi': 345, 'Panvel': 318, 'Thane': 399, 'Jabalpur': 189, 'Kota': 246, 'Rohtak': 353, 'Rajkot': 341, 'Varanasi': 427, '24 Pargana': 0, 'Banka': 45, 'Nagpur': 292, 'Banki': 46, 'Pali': 314, 'Chhatarpur': 101, 'Katihar': 230, 'Mohali': 274, 'Rudrapur': 355, 'Coimbatore': 109, 'Jajpur': 193, 'Mysore': 287, 'Adoni': 3, 'Bikaner': 81, 'Malout': 260, 'Jammu': 198, 'Rajnandgaon': 342, 'Unnao': 420, 'Godhara': 160, 'Kolhapur': 242, 'Satara': 366, 'Siwan': 386, 'Dadra & Nagar Haveli': 111, 'Bhiwani': 72, 'Koppal': 245, 'Nizamabad': 307, 'Madurai': 259, 'Ujjain': 417, 'Palakkad': 311, 'Tiruvallur': 409, 'Panchkula': 316, 'Nanjangud': 297, 'Jhansi': 206, 'Sonipat': 390, 'Puttur': 333, 'Hoshiarpur': 180, 'Gohana': 161, 'Gautam Buddha Nagar': 155, 'Durgapur': 135, 'Palwal': 315, 'Chatrapur': 98, 'Howrah': 183, 'Jind': 209, 'Hubli': 184, 'Panipat': 317, 'Bharatpur': 63, 'Vellore': 430, 'Ambala': 17, 'Guwahati': 168, 'Gangtok': 154, 'Rajahmundry': 340, 'Tiruchirappalli': 406, 'Belgaum': 58, 'Balaghat': 40, 'Jatani': 202, 'Asansol': 31, 'Bilaspur': 82, 'Thanjavur': 401, 'Raigarh(mh)': 337, 'Mandi Dabwali': 263, 'Basti': 55, 'Bolpur': 85, 'Aligarh': 12, 'Balrampur': 43, 'Ratnagiri': 351, 'Muktsar': 281, 'Baran': 49, 'Haldwani': 170, 'Thiruvananthapuram': 403, 'Indore': 188, 'Buxar': 90, 'Chaksu': 94, 'Haridwar': 174, 'Bharuch': 64, 'Muvattupuzha': 284, 'Patna': 322, 'Simdega': 381, 'Singhbhum': 382, 'Bardhaman': 51, 'Pathankot': 320, 'Kharar': 237, 'Silchar': 378, 'Jhalawar': 205, 'Roorkee': 354, 'Saharanpur': 357, 'Solapur': 388, 'Gwalior': 169, 'Alibag': 11, 'Katni': 231, 'Khedbrahma': 239, 'Valsad': 424, 'Satna': 367, 'Hooghly': 179, 'Gurdaspur': 166, 'Dadri': 112, 'Amravati': 20, 'Durg': 134, 'Mehsana': 272, 'Lansdowne': 254, 'Cuttack': 110, 'Jaisalmer': 192, 'Hanumangarh': 173, 'Dungarpur': 133, 'Sri Ganganagar': 391, 'Margao': 268, 'Chinsurah': 106, 'Bhatinda': 65, 'Sibsagar': 376, 'Khalilabad': 233, 'Dehradun': 117, 'Anand': 22, 'Sambalpur': 360, 'Ankleshwar': 27, 'Purnia': 332, 'Tiruverkadu': 410, 'Bahadurgarh': 38, 'Udaipur': 413, 'Jodhpur': 211, 'Sheikhpura': 370, 'Pondicherry': 326, 'Sirsa': 383, 'Godavari': 159, 'Ajmer': 8, 'Moradabad': 276, 'Raipur': 338, 'Navsari': 302, 'Herbertpur': 175, 'Jamshedpur': 200, 'Ramanagar': 344, 'Berhampur': 61, 'Vijayawada': 432, 'Murad Nagar': 283, 'Chandrapur': 97, 'Jamtara': 201, 'Uppidamangalam': 421, 'Nalagarh': 294, 'Una': 419, 'Chakan': 93, 'Idukki': 186, 'Shivpuri': 374, 'Arkalgud': 29, 'Bidar': 77, 'Rupnagar': 356, 'Deoghar': 119, 'Kanchipuram': 219, 'Vapi': 426, 'Medak': 270, 'Kasargode': 227, 'Dhanbad': 123, 'Dakshina Kannada': 113, 'Ganaur': 148, 'Jamalpur': 197, 'Amraoti': 19, 'Mangalore': 265, 'Deolali': 120, 'Gandhinagar': 150, 'Chitradurga': 107, 'Chinchwad': 105, 'Jhajjar': 204, 'Jagdalpur': 190, 'Ranoli': 349, 'Raiwala': 339, 'Guntur': 165, 'Badarpur': 34, 'Adalaj': 2, 'Alipore': 13, 'Bhawani Mandi': 67, 'Mughalsarai': 280, 'Kollam': 244, 'Farukhabad': 143, 'Thiruvallur': 402, 'Udaipurwati': 414, 'Rasra': 350, 'Latur': 255, 'Krishna': 249, 'Gangaikondan': 152, 'Warangal': 438, 'Uluberia': 418, 'Poonamallee': 327, 'Nagaon': 290, 'Hissar': 177, 'Kanyakumari': 222, 'Morbi': 277, 'Bankura': 47, 'Virar': 434, 'Tikamgarh': 405, 'Sultanpur': 393, 'Tirunelveli': 407, 'Bihar Shariff': 78, 'Goa-panaji': 158, 'Ganganagar': 153, 'Kolar': 241, 'Bahadurpur': 39, 'Batala': 56, 'Budhlada': 86, 'Muzaffarnagar': 285, 'Adyar': 4, 'Calicut': 91, 'Raigarh': 336, 'Sonepat': 389, 'Chikkaballapur': 104, 'Kasba': 228, 'Bulandshahr': 87, 'Burdwan': 89, 'Anjar': 26, 'Marandahalli': 267, 'Badaun': 35, 'Namakkal': 295, 'Puri': 331, 'Alwar': 16, 'Surendranagar': 396, 'Khandela': 234, 'Kullu': 251, 'Mohammadabad': 275, 'Sangareddy': 362, 'Ghazipur': 157, 'Shimla': 372, 'Azamgarh': 33, 'Chenani': 99, 'Kanpur Nagar': 221, 'Trivandrum': 411, 'Secunderabad': 368, 'Kurukshetra': 253, 'Dhariawad': 125, 'Bargarh': 53, 'Gadarpur': 145, 'Chikamaglur': 103, 'Karim Nagar': 223, 'Kotdwar': 247, 'Jalaun': 195, 'Parola': 319, 'Bareilly': 52, 'Salem': 358, 'Indi': 187, 'Muzaffarpur': 286, 'Nayagarh': 304, 'Jalgaon': 196, 'Ambikapur': 18, 'Udupi': 416, 'Junagadh': 213, 'Dibrugarh': 131, 'Faridkot': 141, 'Naraingarh': 298, 'Karwar': 226, 'Sant Kabir Nagar': 365, 'Viramgam': 433, 'Manali': 261, 'Gadwal': 147, 'Honavar': 178, 'Mathura': 269, 'Khandwa': 235, 'Solan': 387, 'Sitapur': 385, 'Betul': 62, 'Anantapur': 23, 'Sholapur': 375, 'Pinjore': 325, 'Qadian': 334, 'Sangrur': 364, 'Jorhat': 212, 'Palanpur': 313, 'Narnaul': 299, 'Palamu': 312, 'Falakata': 139, 'Ferozepur': 144, 'Porbandar': 328, 'Dwarka': 136, 'Rangpo': 347, 'Cannanore (kannur)': 92, 'Churu': 108, 'Baghpat': 37, 'Jhumri Tilaiya': 207, 'Naihati': 293, 'Virudhunagar': 435, 'Dharmavaram': 127, 'Darbhanga': 114, 'Nawanshahr': 303, 'Sangli': 363, 'Suri': 397, 'Yamuna Nagar': 440, 'Vasai': 428, 'Aluva': 15, 'Sirsi': 384, 'Bijapur': 79, 'Krishnagar': 250, 'Bhiwadi': 70, 'Bellary': 59, 'Erode': 138, 'Aquem': 28, 'Nellore': 306, 'Udhampur': 415, 'Dhamtari': 122, 'Vandalur': 425, 'Motihari': 278, 'Dharwar': 129, 'Shimoga': 373, 'Jhunjhunu': 208, 'Bijnor': 80, 'Yemmiganur': 441, 'Bokaro': 84, 'Kurnool': 252, 'Srinagar': 392, 'Ranip': 348, 'Davanagere': 115, 'Rajouri': 343, 'Begusarai': 57, 'Goregaon': 164, 'Bally': 41, 'Kachchh': 214, 'Nagaur': 291, 'Anekal': 25, 'Mansa': 266, 'Nanded': 296, 'Dharamasala': 124, 'Chhindwara': 102, 'Jamnagar': 199, 'Zirakpur': 442, 'Abohar': 1, 'Barabanki': 48, 'Nabha': 288, 'Kadapa': 215, 'Perumbavoor': 323, 'Sundargarh': 394, 'Nazira': 305, 'Pratapgarh': 329, 'Dharmapuri': 126, 'Thangadh': 400, 'Lonavala': 256, 'Vizianagaram': 437, 'Kathua': 229, 'Deesa': 116, 'Tiruppur': 408, 'Gadchiroli': 146, 'Gangaghat': 151, 'Bhuj': 76, 'Vastral': 429, 'Phagwara': 324, 'Kheda': 238, 'Swaimadhopur': 398, 'Kharagpur': 236, 'Jobner': 210, 'Gondia': 162, 'Bundi': 88, 'Hamirpur': 171, 'Dongargaon': 132, 'Mubarakpur': 279, 'Tumkur': 412, 'Sanand': 361, 'Kartarpur': 225, 'Bhavnagar': 66, 'Farrukhabad': 142, 'Kadi': 216, 'Seppa': 369, 'Challakere': 95, 'Dhubri': 130, 'Deoria': 121, 'Akot': 9, 'Alappuzha': 10, 'Bhiwandi': 71, 'Shillong': 371, 'Osmanabad': 309, 'Kendua': 232, 'Uran': 422, 'Jaunpur': 203, 'Hisar': 176, 'Bodhan': 83, 'Bhubaneswar': 75, 'Raiganj': 335, 'Bhilai Nagar': 68, 'Baloda': 42, 'Anantnag': 24, 'Berhampore': 60, 'Silvasa': 380, 'Hospet': 181, 'Palai': 310, 'Sidhi': 377}

dctownerbike = {'First Owner': 0, 'Second Owner': 2, 'Third Owner': 3, 'Fourth Owner Or More': 1}

# ----list data for bike------
bikelist = ['TVS Star City Plus Dual Tone 110cc', 'Royal Enfield Classic 350cc', 'Triumph Daytona 675R', 'TVS Apache RTR 180cc', 'Yamaha FZ S V 2.0 150cc-Ltd. Edition', 'Yamaha FZs 150cc', 'Honda CB Hornet 160R  ABS DLX', 'Hero Splendor Plus Self Alloy 100cc', 'Royal Enfield Thunderbird X 350cc', 'Royal Enfield Classic Desert Storm 500cc', 'Yamaha YZF-R15 2.0 150cc', 'Yamaha FZ25 250cc', 'Bajaj Pulsar NS200', 'Bajaj Discover 100M', 'Bajaj Discover 125M', 'Bajaj Pulsar NS200 ABS', 'Bajaj Pulsar RS200 ABS', 'Suzuki Gixxer SF 150cc', 'Benelli 302R 300CC', 'Hero Splendor iSmart Plus IBS 110cc', 'Royal Enfield Classic Chrome 500cc', 'Yamaha FZ V 2.0 150cc', 'Hero Super Splendor 125cc', 'Honda CBF Stunner 125cc', 'Bajaj Pulsar 150cc', 'Honda X-Blade 160CC ABS', 'Bajaj Avenger 220cc', 'KTM RC 390cc', 'Honda CB Unicorn 150cc', 'KTM Duke 200cc', 'Honda CBR 150R 150cc', 'Royal Enfield Thunderbird X 500cc', 'KTM RC 200cc ABS', 'Royal Enfield Thunderbird 350cc', 'Royal Enfield Bullet Electra 350cc', 'Bajaj Avenger Street 220 ABS', 'Mahindra Centuro NXT 110cc', 'Hero Hunk 150cc', 'Suzuki Gixxer SF Fi 150cc SP ABS', 'Yamaha FZ 150cc', 'Royal Enfield\u200e Bullet 350cc', 'TVS Apache RTR 160cc', 'Honda CB Shine 125cc', 'Benelli TNT 600i ABS', 'Honda Dream Yuga 110cc', 'Yamaha SZ 150cc', 'Suzuki Gixxer 150cc', 'Bajaj Avenger Cruise 220', 'Kawasaki Z900', 'Bajaj Pulsar 220cc', 'Hero CD Deluxe 100cc', 'Kawasaki Ninja 650cc', 'Bajaj Platina 125cc', 'Hero Karizma ZMR 223cc', 'Bajaj Pulsar 180cc', 'Yamaha FZ25 ABS 250cc', 'Bajaj CT 100 100cc', 'Royal Enfield Interceptor 650cc', 'KTM Duke 250cc', 'Royal Enfield Himalayan 410cc', 'Bajaj Pulsar 135LS', 'Bajaj Pulsar 220F', 'Yamaha FZ16 150cc', 'Ducati Scrambler 1100 Special', 'Triumph Street Triple 765', 'Bajaj V15 150cc', 'Suzuki Gixxer Fi 150cc ABS', 'Hero Splendor plus 100cc', 'KTM Duke 390cc', 'Honda CBR 250R', 'Bajaj Pulsar RS200', 'Benelli TNT 600i', 'Suzuki Gixxer 150cc SP Rear Disc', 'Yamaha FZ S V 2.0 150cc', 'Royal Enfield Classic 500cc', 'Hyosung GT650R', 'Yamaha YZF-R15 S 150cc', 'TVS Apache RTR 160 4V Disc', 'Benelli TNT 300', 'Honda CB ShineSP 125cc', 'Hero Passion Pro 100cc', 'Hero Splendor Plus 100cc', 'Yamaha YZF R6 600cc', 'Ducati 1299 Superleggera', 'Royal Enfield Electra 350cc', 'TVS Phoenix Disc 125cc', 'Harley-Davidson Street 750', 'Royal Enfield Himalayan 410cc Fi ABS', 'Bajaj Discover 150cc', 'Bajaj Avenger Street 220', 'Royal Enfield Standard 350cc', 'Honda CB Shine 125cc Disc', 'Honda CB Unicorn ABS 150cc', 'Yamaha YZF-R15 V3 150cc', 'Bajaj Pulsar NS 200', 'Bajaj Dominar 400', 'Honda X-Blade 160cc', 'Suzuki Hayabusa 1300cc', 'Ducati Monster 821 Dark', 'Yamaha FZ S V 2.0 150cc Rear Disc', 'Suzuki Gixxer SF 150cc Special MOTOGP Edition Rear Disc', 'KTM RC 200cc', 'Bajaj Discover 125ST', 'Hero Splendor Plus Kick Alloy 100cc', 'Hero Karizma 223cc', 'Hero Splendor 100cc', 'Ducati 1198 SP 1198cc', 'Royal Enfield Bullet 500cc', 'Yamaha Fazer 150cc', 'Yamaha Gladiator 125cc', 'Hero Karizma R 223cc', 'Harley-Davidson Iron 883', 'TVS Apache RTR 200 4V Fi', 'TVS Apache RTR 160 4V DISC ABS BS6', 'Bajaj Dominar 400 ABS', 'Royal Enfield Classic Gunmetal Grey 350cc', 'Hero HF Deluxe i3s iBS 100cc', 'Suzuki Gixxer SF Fi 150cc ABS', 'Hero Splendor iSmart 110cc', 'Bajaj Platina 100cc', 'TVS Apache RTR 200 4V FI', 'Royal Enfield Bullet Twinspark 350cc', 'TVS Star City 110cc', 'Bajaj Platina  Alloy ES-100cc', 'Ducati Panigale 959', 'Royal Enfield Classic 350cc-Redditch Edition', 'TVS Sport 100cc', 'Bajaj Pulsar AS200', 'Royal Enfield Classic Desert Storm 500cc Dual Disc', 'Honda Livo 110cc', 'Suzuki Gixxer SF 150cc SP Rear Disc', 'Yamaha SZ-RR 150cc', 'Royal Enfield Thunderbird 500cc', 'Royal Enfield Bullet Electra Twinspark 350cc', 'Bajaj Discover 150F Disc', 'Yamaha Saluto 125cc Disc Special Edition', 'Triumph Street Triple ABS 675cc', 'Honda CBR 250R ABS', 'Hyosung Aquila GV250', 'Jawa Forty Two 295CC', 'Bajaj V12 125cc', 'Bajaj V12 125cc Disc', 'Yamaha Fazer 25 250cc', 'Hero Xpulse 200T', 'Honda CB Hornet 160R CBS', 'Suzuki Gixxer 150cc SP ABS', 'Hero Passion Xpro 110cc', 'Yamaha YZF-R3 320cc ABS', 'Royal Enfield Bullet 350 cc', 'Hero HF Deluxe 100cc', 'Honda CB Twister 110cc', 'Bajaj Pulsar 125cc Disc CBS', 'Honda CB Shine 125cc Drum BS6', 'Honda CB Hornet 160R STD', 'Honda Dream Neo 110cc', 'BMW G 310 R', 'Bajaj Pulsar AS150', 'Kawasaki Ninja 250cc', 'Benelli TNT 899', 'Indian Chief Classic 1800cc', 'Hero Achiever 150cc', 'TVS Apache 150cc', 'Kawasaki ER-6n 650cc', 'Hero HF Deluxe Self 100cc', 'Bajaj Pulsar NS160', 'Royal Enfield Classic Gunmetal Grey 350cc ABS', 'Suzuki Intruder 150cc', 'TVS Apache RTR 200 4V ABS Race Edition', 'Bajaj CT 100 B', 'Hero Passion Pro 110cc Drum', 'Yamaha YZF-R15 150cc', 'TVS Apache RTR 160 4V DISC ABS', 'Mahindra Mojo 300cc', 'TVS Apache RTR 200 4V Carburetor', 'Hero Ignitor Disc 125cc', 'Bajaj Avenger Street 150', 'Royal Enfield Continental GT 535cc', 'Hero Glamour Disc 125cc', 'Suzuki Gixxer SF Fi 150cc', 'Hero HF Dawn 100cc', 'Suzuki Slingshot Plus 125cc', 'Mahindra Centuro Rockstar 110cc', 'Mahindra Centuro 110cc', 'Honda CB Hornet 160R Special Edition STD', 'Harley-Davidson Street Rod XG750A ABS', 'Hero Splendor Plus IBS i3S 100cc', 'Bajaj Discover 135cc', 'Bajaj Discover 125cc', 'TVS Apache RTR 160 4V DRUM ABS', 'Honda CB Unicorn 160 CBS', 'KTM Duke 125cc', 'Bajaj Boxer BM150', 'Hero Glamour 125cc', 'Bajaj Discover 100cc', 'Bajaj Avenger Street 180', 'TVS Star City Plus 110cc', 'Honda CB Trigger 150cc', 'Kawasaki Ninja 650 KRT Edition', 'Bajaj Platina 100cc ComforTec Alloy', 'Benelli TNT R 1130cc', 'Honda CB Unicorn Dazzler 150cc', 'Benelli TNT 600 GT', 'Hyosung GT250R', 'Yamaha YZF-R1 1000cc', 'Hero Xtreme 200R', 'Ducati Diavel 1200cc', 'Triumph Speed Triple 1050cc', 'Indian Scout Bobber 1130cc', 'Bajaj V15 150cc POWER UP', 'Jawa Standard 295CC', 'Yamaha SZR 150cc', 'TVS Star Sport 100cc', 'Hyosung Aquila 250 250cc', 'Kawasaki Z650', 'Hero CD Dawn 100cc', 'TVS Apache RTR 200 4V ABS', 'Hero Passion 100cc', 'Suzuki Intruder SP 150cc', 'Yamaha YZF-R3 320cc', 'TVS Apache RR310', 'Hero Passion Plus 100cc', 'Royal Enfield Classic 350cc-Redditch Edition Dual Disc', 'Hero CBZ 150cc', 'Yamaha FZS FI 150cc', 'Honda CB Unicorn 160 STD', 'Suzuki GS 150 R 150cc', 'Royal Enfield Machismo 500cc', 'Hero CBZ Xtreme 150cc', 'Yamaha SZ RR V 2.0 150cc', 'TVS Apache RTR 180cc ABS', 'Hero Honda Splendor 100cc', 'Honda CBR 150R Deluxe', 'Hero Ignitor 125cc', 'Bajaj Pulsar 200cc', 'Kawasaki Ninja 300cc', 'Kawasaki Ninja 300 ABS', 'Bajaj Pulsar 150cc Rear Disc', 'Hero Splendor NXG 100cc', 'Hero Achiever Disc 150cc', 'TVS Apache RTR 200 4V Carburetor Race Edition 2.0', 'Royal Enfield Thunderbird 350cc ABS', 'Harley-Davidson Street 750 ABS', 'Bajaj Pulsar 150cc Rear Disc ABS', 'KTM Duke 250cc ABS', 'Bajaj Pulsar 200 NS 200cc', 'Mahindra Mojo Tourer Edition 300cc', 'Hero Passion Pro i3S Alloy 100cc', 'Royal Enfield Thunderbird X 350cc ABS', 'Hero Xtreme 150cc', 'Bajaj Boxer CT100', 'Royal Enfield Bullet 350cc', 'Royal Enfield Standard 500cc', 'Hyosung Aquila Pro GV650', 'Royal Enfield Classic 500cc Dual Disc', 'Suzuki V-Strom 1000cc', 'KTM RC 125CC', 'Suzuki Gixxer SF 250cc ABS', 'Harley-Davidson 1200 Custom', 'Honda Dream Yuga 110cc CBS', 'Hero Splendor Pro 100cc', 'Suzuki Hayate 110cc', 'Yamaha Fazer FI V 2.0 150cc', 'TVS Victor 110cc Disc', 'Royal Enfield Classic Stealth Black 500cc', 'TVS Apache RTR 200 4V Dual Channel ABS BS6', 'Honda CB Shine 125cc CBS', 'Honda Livo Disc 110cc', 'Bajaj Discover 110cc', 'Suzuki Gixxer SF 150cc ABS', 'Hero CD 100SS', 'Hero Honda Splendor Plus 100cc', 'Bajaj Discover 100T', 'Hero HF Deluxe self Alloy 100cc', 'Benelli TNT 25 250cc', 'Yamaha MT-15 150cc', 'Yamaha FZS FI 150cc Rear Disc', 'TVS Apache RTR 200 4V Carburetor Pirelli Tyres', 'Triumph Tiger 800 XRX', 'Ducati XDiavel 1262CC S', 'TVS Suzuki Shogun 110cc', 'Bajaj Discover 125cc Disc', 'Triumph Thunderbird Storm 1700cc', 'Suzuki GSX-S750', 'TVS Flame 125cc', 'Triumph Tiger 800 XCA', 'Royal Enfield Machismo 350cc', 'TVS Victor 110cc', 'Honda CBR650R', 'Hero Xpulse 200cc FI', 'Hero HF Deluxe i3s 100cc', 'TVS Apache RTR 160cc Matt Red Rear Disc', 'Rajdoot GTX 175cc', 'Hero Xtreme 200R ABS', 'Honda CB Unicorn 160', 'Honda CB Hornet 160R Special Edition-CBS', 'TVS Apache RTR 200 4V Carburetor Pirelli Tyres Race Edition 2.0', 'TVS Apache RR310 Slipper Clutch', 'Mahindra Mojo UT300', 'Royal Enfield Bullet Twinspark Kickstart 350cc', 'Bajaj Pulsar  180cc', 'Honda CD 110 Dream', 'Royal Enfield Bullet Twinspark 500cc', 'Hero Xtreme Sports Rear Disc 150cc', 'Bajaj CT 100 ES Alloy', 'Bajaj  Pulsar 180cc', 'Bajaj Discover 150F', 'Hyosung GT 650N', 'Triumph Street Twin 900cc', 'Bajaj CT 100 Alloy', 'TVS Apache RTR 160 4V Drum', 'Yamaha SZ RR V 2.0 150cc Limited Edition', 'Yamaha YZF-R1M 1000cc', 'Hero Glamour i3s 125cc', 'Harley-Davidson Roadster XL 1200CX', 'Triumph Tiger 800 XR', 'KTM Duke 200cc ABS', 'Honda CBR1000RR Fireblade', 'Honda SP125 Disc BS6', 'Bajaj Platina 110 H Gear Disc', 'Hero Splendor Plus 100 cc', 'Honda CBR 250R Repsol', 'Triumph Bonneville T100 865cc', 'Yamaha RX135 135cc 4-Speed', 'Benelli 302R', 'Hero Splendor iSmart 100cc', 'Royal Enfield Classic 350cc Dual Disc', 'Honda CB 1000R', 'Honda CBR 600RR', 'Ducati Monster 797', 'Ducati Monster 1200', 'Suzuki GSX-R 1000cc', 'Ducati Monster 796 Corse Stripe', 'TVS Victor 110cc Disc SBT', 'Honda CB ShineSP 125cc CBS Disc', 'Kawasaki Z250', 'Royal Enfield Classic Squadron Blue 500cc', 'Suzuki Gixxer 150cc Dual Tone Rear Disc', 'TVS Apache RTR 200 4V', 'Honda Livo Disc 110cc CBS', 'TVS Apache RTR 160cc Rear Disc', 'Yamaha FZ S V 3.0 150cc', 'BMW G 310 GS', 'Royal Enfield Classic 350cc Signals Edition', 'Royal Enfield Bullet Electra Twinspark 350cc Double Disc', 'Honda CB Hornet 160R 160cc STD', 'Suzuki Intruder 150cc FI', 'Bajaj Platina 110 CBS', 'Hero Xtreme Sports 150cc', 'Bajaj Avenger Cruise 220 ABS', 'Honda CB Hornet 160R 160cc STD SP', 'Kawasaki Versys 650cc', 'Ducati Multistrada 1200 Enduro', 'Hero Passion Pro i3S Alloy 100cc IBS', 'Hero Xtreme Sports 149cc', 'TVS Apache RTR 160 4V Carburetor', 'Triumph Thruxton R 1200cc', 'Honda CD 110 Dream DX', 'BMW S 1000 XR Pro', 'Honda CB ShineSP 125cc Disc', 'Hero HF Deluxe Eco 100cc', 'Bajaj XCD 125', 'Honda CB ShineSP 125cc CBS', 'Bajaj CT110 ES Alloy', 'TVS Apache RTR 160 4V FI', 'Triumph Bonneville T100 900cc', 'Bajaj Avenger Street 160 ABS', 'TVS Apache RTR 160cc White Race Edition Rear Disc', 'Royal Enfield Himalayan 410cc Sleet Edition', 'Hero Splendor+ 100cc', 'Suzuki Gixxer SF 150cc Rear Disc', 'TVS Apache RTR 160 4V Carburetor With Rear Disc', 'Suzuki Heat 125cc', 'Honda CB Hornet 160R  ABS STD', 'Yamaha Fazer25 250cc', 'Bajaj Pulsar NS160 Rear Disc', 'Honda CB Hornet 160R', 'Bajaj Discover150 150cc', 'Bajaj Discover 125T', 'Bajaj Pulsar 150cc Classic', 'Yamaha Saluto 125cc', 'Hero Passion XPRO 110 cc', 'Yamaha FZS FI 150cc Special Edition', 'TVS Fiero 150cc', 'Mahindra Mojo XT300', 'Bajaj Platina Alloy ES 100cc', 'TVS Jive 110cc', 'Bajaj Boxer AT100', 'Bajaj Discover 150S Disc', 'TVS Radeon 110cc Drum SBT', 'Honda CD 110 Dream Self', 'Suzuki Gixxer 150cc ABS', 'Suzuki Hayate EP 110cc', 'Yamaha SZX 150cc', 'Hero CBZ Star 160cc', 'Hero Passion PRO  100 cc', 'Hero Passion Pro i3S Disc 100cc', 'Bajaj Avenger 200cc', 'Hero Honda Ambition 135cc', 'Bajaj Pulsar 135LS 135cc', 'Bajaj CT 100 KS Alloy', 'BMW S 1000 RR Pro', 'Kawasaki Versys 1000', 'Honda CB Unicorn 150 150cc', 'Kawasaki Z800', 'Hero Glamour PGM Fi 125cc', 'Royal Enfield Continental GT 650cc', 'LML Freedom DX 110cc', 'Harley-Davidson XG750 750cc', 'Yezdi Classic 250cc', 'Hero Passion Pro 100cc Drum Alloy', 'TVS Star 100cc', 'Bajaj XCD 135', 'Bajaj Avenger 150cc', 'Hero HF Deluxe 100 cc', 'Yamaha Fazer FI 150cc', 'TVS Apache RTR 200 4V FI Race Edition 2.0', 'Yamaha FZ V 3.0 150cc', 'Hero Super Splendor 125cc i3s', 'Yamaha SS 125 125cc', 'Suzuki Gixxer SF 150cc Special MOTOGP Edition', 'TVS Victor GX 110cc', 'TVS Apache RTR 200 4V Race Edition 2.0', 'Hero Passion Pro TR 100cc', 'Honda CBR 650 F', 'Yamaha FZ S V 3.0 150cc ABS Dark Knight BS VI', 'Hero HF Deluxe Self Spoke 100cc', 'TVS Sports plus ES 100cc', 'BMW F750 GS 850cc', 'Royal Enfield Bullet Electra Twinspark 350CC ABS', 'Hero Glamour Fi 125cc', 'Royal Enfield Himalayan 410cc Sleet ABS', 'Bajaj Pulsar NS 200cc', 'Yamaha YBR 110cc', 'Bajaj CT 100 Spoke', 'Yamaha Crux 110cc', 'Yamaha Saluto RX 110cc', 'MV Agusta Brutale 1090', 'Royal Enfield Himalayan 410cc Fi', 'MV Agusta F3 800cc', 'Kawasaki Ninja 400', 'Benelli TRK 502X', 'TVS Phoenix 125cc', 'Harley-Davidson Fat Bob 107 Ci', 'TVS Apache RTR 160cc White Race Edition', 'Ideal Jawa Yezdi CL-II 250 cc', 'Hero Splendor Pro Classic 100cc', 'Yamaha FZ Fi Version 2.0 150cc', 'Yamaha SZS 150cc', 'Triumph Daytona 675 ABS', 'Royal Enfield Classic Chrome 500cc ABS', 'Harley-Davidson Sportster 883', 'Suzuki Zeus 125cc', 'Yamaha Saluto 125cc-Special Edition', 'Bajaj Avenger 180cc', 'Bajaj Pulsar 150cc Neon', 'Kawasaki Z1000', 'Hero CBZ Xtreme 150 cc', 'Kawasaki Vulcan S 650cc', 'Yamaha RX-Z 135cc', 'Yamaha Libero G5 110cc', 'Bajaj Pulsar RS200  ABS-200cc', 'Bajaj Discover150S 150cc', 'Hero i Smart 125cc', 'Hero Splendor Plus  100 cc', 'Hero Splendor Plus 100 CC', 'Hero Karizma 223 cc', 'TVS MAX 4R 110cc', 'Mahindra Pantero 110cc', 'Hero Ambition 135cc', 'Honda CBR 250R Repsol ABS', 'Hero Hunk Rear Disc 150cc']

brandlist = ['TVS', 'Royal Enfield', 'Triumph', 'Yamaha', 'Honda', 'Hero', 'Bajaj', 'Suzuki', 'Benelli', 'KTM', 'Mahindra', 'Kawasaki', 'Ducati', 'Hyosung', 'Harley-Davidson', 'Jawa', 'BMW', 'Indian', 'Rajdoot', 'LML', 'Yezdi', 'MV', 'Ideal']

citylist = ['Ahmedabad', 'Delhi', 'Bangalore', 'Mumbai', 'Kalyan', 'Faridabad', 'Mettur', 'Hyderabad', 'Kaithal', 'Gurgaon', 'Pune', 'Noida', 'Nashik', 'Kochi', 'Allahabad', 'Samastipur', 'Nadiad', 'Lucknow', 'Jaipur', 'Karnal', 'Gorakhpur', 'Vidisha', 'Hosur', 'Bagalkot', 'Baripara', 'Agra', 'Dharwad', 'Vadodara', 'Jalandhar', 'Surat', 'Chennai', 'Navi Mumbai', 'Gandhidham', 'Visakhapatnam', 'Thrissur', 'Kolkata', 'Ernakulam', 'Barasat', 'Ghaziabad', 'Bhubaneshwar', 'Amritsar', 'Bhopal', 'Hamirpur(hp)', 'Kottayam', 'Arrah', 'Patiala', 'Ranga Reddy', 'Mandi', 'Ludhiana', 'Mandya', 'Siliguri', 'Aurangabad', 'Kanpur', 'Bhilwara', 'Meerut', 'Rewari', 'Ahmednagar', 'Wardha', 'Chandigarh', 'Ranchi', 'Panvel', 'Thane', 'Jabalpur', 'Kota', 'Rohtak', 'Rajkot', 'Varanasi', '24 Pargana', 'Banka', 'Nagpur', 'Banki', 'Pali', 'Chhatarpur', 'Katihar', 'Mohali', 'Rudrapur', 'Coimbatore', 'Jajpur', 'Mysore', 'Adoni', 'Bikaner', 'Malout', 'Jammu', 'Rajnandgaon', 'Unnao', 'Godhara', 'Kolhapur', 'Satara', 'Siwan', 'Dadra & Nagar Haveli', 'Bhiwani', 'Koppal', 'Nizamabad', 'Madurai', 'Ujjain', 'Palakkad', 'Tiruvallur', 'Panchkula', 'Nanjangud', 'Jhansi', 'Sonipat', 'Puttur', 'Hoshiarpur', 'Gohana', 'Gautam Buddha Nagar', 'Durgapur', 'Palwal', 'Chatrapur', 'Howrah', 'Jind', 'Hubli', 'Panipat', 'Bharatpur', 'Vellore', 'Ambala', 'Guwahati', 'Gangtok', 'Rajahmundry', 'Tiruchirappalli', 'Belgaum', 'Balaghat', 'Jatani', 'Asansol', 'Bilaspur', 'Thanjavur', 'Raigarh(mh)', 'Mandi Dabwali', 'Basti', 'Bolpur', 'Aligarh', 'Balrampur', 'Ratnagiri', 'Muktsar', 'Baran', 'Haldwani', 'Thiruvananthapuram', 'Indore', 'Buxar', 'Chaksu', 'Haridwar', 'Bharuch', 'Muvattupuzha', 'Patna', 'Simdega', 'Singhbhum', 'Bardhaman', 'Pathankot', 'Kharar', 'Silchar', 'Jhalawar', 'Roorkee', 'Saharanpur', 'Solapur', 'Gwalior', 'Alibag', 'Katni', 'Khedbrahma', 'Valsad', 'Satna', 'Hooghly', 'Gurdaspur', 'Dadri', 'Amravati', 'Durg', 'Mehsana', 'Lansdowne', 'Cuttack', 'Jaisalmer', 'Hanumangarh', 'Dungarpur', 'Sri Ganganagar', 'Margao', 'Chinsurah', 'Bhatinda', 'Sibsagar', 'Khalilabad', 'Dehradun', 'Anand', 'Sambalpur', 'Ankleshwar', 'Purnia', 'Tiruverkadu', 'Bahadurgarh', 'Udaipur', 'Jodhpur', 'Sheikhpura', 'Pondicherry', 'Sirsa', 'Godavari', 'Ajmer', 'Moradabad', 'Raipur', 'Navsari', 'Herbertpur', 'Jamshedpur', 'Ramanagar', 'Berhampur', 'Vijayawada', 'Murad Nagar', 'Chandrapur', 'Jamtara', 'Uppidamangalam', 'Nalagarh', 'Una', 'Chakan', 'Idukki', 'Shivpuri', 'Arkalgud', 'Bidar', 'Rupnagar', 'Deoghar', 'Kanchipuram', 'Vapi', 'Medak', 'Kasargode', 'Dhanbad', 'Dakshina Kannada', 'Ganaur', 'Jamalpur', 'Amraoti', 'Mangalore', 'Deolali', 'Gandhinagar', 'Chitradurga', 'Chinchwad', 'Jhajjar', 'Jagdalpur', 'Ranoli', 'Raiwala', 'Guntur', 'Badarpur', 'Adalaj', 'Alipore', 'Bhawani Mandi', 'Mughalsarai', 'Kollam', 'Farukhabad', 'Thiruvallur', 'Udaipurwati', 'Rasra', 'Latur', 'Krishna', 'Gangaikondan', 'Warangal', 'Uluberia', 'Poonamallee', 'Nagaon', 'Hissar', 'Kanyakumari', 'Morbi', 'Bankura', 'Virar', 'Tikamgarh', 'Sultanpur', 'Tirunelveli', 'Bihar Shariff', 'Goa-panaji', 'Ganganagar', 'Kolar', 'Bahadurpur', 'Batala', 'Budhlada', 'Muzaffarnagar', 'Adyar', 'Calicut', 'Raigarh', 'Sonepat', 'Chikkaballapur', 'Kasba', 'Bulandshahr', 'Burdwan', 'Anjar', 'Marandahalli', 'Badaun', 'Namakkal', 'Puri', 'Alwar', 'Surendranagar', 'Khandela', 'Kullu', 'Mohammadabad', 'Sangareddy', 'Ghazipur', 'Shimla', 'Azamgarh', 'Chenani', 'Kanpur Nagar', 'Trivandrum', 'Secunderabad', 'Kurukshetra', 'Dhariawad', 'Bargarh', 'Gadarpur', 'Chikamaglur', 'Karim Nagar', 'Kotdwar', 'Jalaun', 'Parola', 'Bareilly', 'Salem', 'Indi', 'Muzaffarpur', 'Nayagarh', 'Jalgaon', 'Ambikapur', 'Udupi', 'Junagadh', 'Dibrugarh', 'Faridkot', 'Naraingarh', 'Karwar', 'Sant Kabir Nagar', 'Viramgam', 'Manali', 'Gadwal', 'Honavar', 'Mathura', 'Khandwa', 'Solan', 'Sitapur', 'Betul', 'Anantapur', 'Sholapur', 'Pinjore', 'Qadian', 'Sangrur', 'Jorhat', 'Palanpur', 'Narnaul', 'Palamu', 'Falakata', 'Ferozepur', 'Porbandar', 'Dwarka', 'Rangpo', 'Cannanore (kannur)', 'Churu', 'Baghpat', 'Jhumri Tilaiya', 'Naihati', 'Virudhunagar', 'Dharmavaram', 'Darbhanga', 'Nawanshahr', 'Sangli', 'Suri', 'Yamuna Nagar', 'Vasai', 'Aluva', 'Sirsi', 'Bijapur', 'Krishnagar', 'Bhiwadi', 'Bellary', 'Erode', 'Aquem', 'Nellore', 'Udhampur', 'Dhamtari', 'Vandalur', 'Motihari', 'Dharwar', 'Shimoga', 'Jhunjhunu', 'Bijnor', 'Yemmiganur', 'Bokaro', 'Kurnool', 'Srinagar', 'Ranip', 'Davanagere', 'Rajouri', 'Begusarai', 'Goregaon', 'Bally', 'Kachchh', 'Nagaur', 'Anekal', 'Mansa', 'Nanded', 'Dharamasala', 'Chhindwara', 'Jamnagar', 'Zirakpur', 'Abohar', 'Barabanki', 'Nabha', 'Kadapa', 'Perumbavoor', 'Sundargarh', 'Nazira', 'Pratapgarh', 'Dharmapuri', 'Thangadh', 'Lonavala', 'Vizianagaram', 'Kathua', 'Deesa', 'Tiruppur', 'Gadchiroli', 'Gangaghat', 'Bhuj', 'Vastral', 'Phagwara', 'Kheda', 'Swaimadhopur', 'Kharagpur', 'Jobner', 'Gondia', 'Bundi', 'Hamirpur', 'Dongargaon', 'Mubarakpur', 'Tumkur', 'Sanand', 'Kartarpur', 'Bhavnagar', 'Farrukhabad', 'Kadi', 'Seppa', 'Challakere', 'Dhubri', 'Deoria', 'Akot', 'Alappuzha', 'Bhiwandi', 'Shillong', 'Osmanabad', 'Kendua', 'Uran', 'Jaunpur', 'Hisar', 'Bodhan', 'Bhubaneswar', 'Raiganj', 'Bhilai Nagar', 'Baloda', 'Anantnag', 'Berhampore', 'Silvasa', 'Hospet', 'Palai', 'Sidhi']

ownerlistbike = ['First Owner', 'Second Owner', 'Third Owner', 'Fourth Owner Or More']


# set page config
st.set_page_config(page_title='TVS CREDIT Vehicle Valuation', page_icon='./logo/api.png', layout='wide')

html = f"""<a href='{'https://www.tvscredit.com/'}'><img src='https://www.tvscredit.com/media/1927/tvs-credit-logo-01.png' width='200' height='50'></a>"""
st.markdown(html, unsafe_allow_html=True)

# st.image('./logo/tvs_logo.png')

    

with st.sidebar:
    selected = option_menu(
        menu_title = 'Menu',
        options = ['Home', 'Car', 'Bike', 'Contact'],
        icons = ['house', '', 'bicycle', 'envelope'],
        menu_icon = 'cast',
    )

# Home Page
if selected == 'Home':
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        else:
            return r.json()
    # API DOC URL FOR CAR
    URL = 'https://tvs-price-predictor.herokuapp.com/docs'
    # API DOC URL FOR BIKE
    URL2 = 'https://tvs-price-predictor-bike.herokuapp.com/docs'

    # ---stack lottie transition---
    lottie_api = load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_8NYY2Y.json')

    with st.container():
        # ------ HEADER SECTION-------
        left_column, right_column = st.columns(2)
        with left_column:
            st.title('TVS CREDIT - Effortless Price Predictions by AI:speech_balloon:')
            st.subheader('As per the trends in market :chart_with_upwards_trend:')
            st.write('''A few years ago, the ratio of new cars to used cars 
            was 1:1.2 which is now at 1:2.2. The used car market in India 
            has been the center of attention in the slow growing 
            automotive industry in India.''')
            st.subheader('How our API is helpful :star:')
            st.write('''Keeping the demand of used cars in mind, 
            This website helps users to predict the price to sell/buy the car
            with the help of AI and ML.''')
            st.subheader('How to use? :hushed:')
            st.write('The API is encoded, only the website can decode and call it.')
            st.write('Check out the API here :fire:')
            st.write('[Learn More >](https://tvs-price-predictor.herokuapp.com/docs)')
        # Lottie element
        with right_column:
            st_lottie(lottie_api, height=300, key='api')

# Car Page
if selected == 'Car':
    st.header('GET THE PRICE OF USED CAR')
    # Form to take data from user
    col1, col2 = st.columns(2)
    with col1:
        with st.form(key='form1'):
            # car = st.text_input('Car Model')
            car = st.selectbox('Car Model', options=carlist)
            car = dctcar[car]
            # location = st.text_input('Location')
            location = st.selectbox('Location', options=loclist)
            location = dctloc[location]
            # year = st.text_input('Year')
            year = st.selectbox('Year', options=yearlist)
            year = dctyear[year]
            km_driven = st.text_input('Kms Driven (Enter accurate value for better results)')
            # owner_type = st.text_input('Owner Type')
            owner_type = st.selectbox('Owner Type', options=ownerlist)
            owner_type = dctowner[owner_type]
            # fuel_type = st.text_input('Fuel Type')
            fuel_type = st.selectbox('Fuel Type', options=fuellist)
            fuel_type = dctfuel[fuel_type]
            power = st.text_input('Power in bhp')
            # power = int(power)
            price = st.text_input('Original Price in lakhs(Example: 13.56 lakhs)')


            # ---Submit Button---
            submit_button = st.form_submit_button(label='Get Car Price')
            # if submit_button:
            #     st.success('Thanks for using!')


            if submit_button and (km_driven=="" or power == "" or price == ""):
                # st.success('Thanks for using!')
                st.warning('You have missed some fields to fill in!')
            elif km_driven=="" or power == "" or price == "":
                st.warning('Please fill out all the fields!')
            else:
                st.success('Thanks for Filling!')
                # ---Calling the API---
                URL = 'https://tvs-price-predictor.herokuapp.com/predict'

                # Best Condition Pred
                PARAMS = {
                "Car": car,
                "Location": location,
                "Year": year,
                "Kilometers_Driven": km_driven,
                "Owner_Type": owner_type,
                "Fuel_Type": fuel_type,
                "Power": power
                }
                # Good condition Pred
                PARAMS2 = {
                "Car": car,
                "Location": location,
                "Year": int(year-3),
                "Kilometers_Driven": km_driven,
                "Owner_Type": owner_type,
                "Fuel_Type": fuel_type,
                "Power": power
                }
                # if submit_button:    
                #     response = requests.post(URL, json=PARAMS)
                    # st.write(response.json()['prediction'])


        # ---Result---
        if submit_button and not (km_driven=="" or power == "" or price == ""):
            # Wait transition
            with st.spinner('Wait for it...'):
                response = requests.post(URL, json=PARAMS)
                response2 = requests.post(URL, json=PARAMS2)
            # st.success('Done!')
            # response = requests.post(URL, json=PARAMS)
            # st.write(response.json()['prediction'])

            # ---Progress bar---
            # Original Price
            org_price = float(price)
            st.write('Original Price', org_price)

            # For Best Price
            resp_result = response.json()['prediction']
            st.write('Best Price ', resp_result)
            my_bar = st.progress(100) # set to original price

            perc_resp = int((resp_result/org_price)*100)
            for percent_complete in range(perc_resp):
                time.sleep(0.001)
                my_bar.progress(percent_complete + 1)

            # For Average Price
            resp_result2 = response2.json()['prediction']
            st.write('Average Price ', resp_result2)
            perc_resp2 = int((resp_result2/org_price)*100)
            my_bar2 = st.progress(100) # set to original price

            for percent_complete in range(perc_resp2):
                time.sleep(0.001)
                my_bar2.progress(percent_complete + 1)
    with col2:
        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            else:
                return r.json()
        lottie_api = load_lottieurl('https://assets5.lottiefiles.com/packages/lf20_kqfglvmb.json')
        st_lottie(lottie_api, height=500, key='api')


if selected == 'Bike':
    st.header('GET THE PRICE OF USED BIKE')
    # Form to take data from user
    col1, col2 = st.columns(2)
    with col1:
        with st.form(key='form2'):
            bike = st.selectbox('Bike Model', options=bikelist)
            bike = dctbike[bike]
            # location = st.text_input('Location')
            city = st.selectbox('Location', options=citylist)
            city = dctcity[city]
            # year = st.text_input('Year')
            bike_year = st.selectbox('Year', options=yearlist)
            if bike_year == 'less than 2003':
                bike_year = 2002   
            age = int(dt.date.today().year)-int(bike_year)                # Present year - selling year
            # Km_driven by bike
            km_driven_bike = st.text_input('Kms Driven (Enter accurate value for better results)')
            # owner_type = st.text_input('Owner Type')
            owner_type_bike = st.selectbox('Owner Type', options=ownerlistbike)
            owner_type_bike = dctownerbike[owner_type_bike]
            # brand of bike
            bike_brand = st.selectbox('Brand', options=brandlist)
            bike_brand = dctbrand[bike_brand]
            # Power of bike (Horse Power)
            bike_power = st.text_input('Power in bhp')
            # power = int(power)
            bike_price = st.text_input('Original Price')


            # ---Submit Button---
            submit_button2 = st.form_submit_button(label='Get Bike Price')
            # if submit_button:
            #     st.success('Thanks for using!')


            if submit_button2 and (km_driven_bike=="" or bike_power == "" or bike_price == ""):
                # st.success('Thanks for using!')
                st.warning('You have missed some fields to fill in!')
            elif km_driven_bike=="" or bike_power == "" or bike_price == "":
                st.warning('Please fill out all the fields!')
            else:
                st.success('Thanks for Filling!')
                # ---Calling the API---
                URL = 'https://tvs-price-predictor-bike.herokuapp.com/bike-predict'

                # Best Condition Pred
                PARAMS = {
                "bike_name": bike,
                "city": city,
                "kms_driven": km_driven_bike,
                "owner": owner_type_bike,
                "age": age,
                "power": bike_power,
                "brand": bike_brand
                }
                # Good condition Pred
                PARAMS2 = {
                "bike_name": bike,
                "city": city,
                "kms_driven": km_driven_bike,
                "owner": owner_type_bike,
                "age": int(int(age)+3),
                "power": bike_power,
                "brand": bike_brand
                }
                # if submit_button:    
                #     response = requests.post(URL, json=PARAMS)
                    # st.write(response.json()['prediction'])


        # ---Result---
        if submit_button2 and not (km_driven_bike=="" or bike_power == "" or bike_price == ""):
            # Wait transition
            with st.spinner('Wait for it...'):
                bike_response = requests.post(URL, json=PARAMS)
                bike_response2 = requests.post(URL, json=PARAMS2)
            # st.success('Done!')
            # response = requests.post(URL, json=PARAMS)
            # st.write(response.json()['prediction'])

            # ---Progress bar---
            # Original Price
            bike_org_price = float(bike_price)
            st.write('Original Price', bike_org_price)

            # For Best Price
            bike_resp_result = bike_response.json()['bike_price_prediction']
            st.write('Best Price ', bike_resp_result)
            my_bar_bike = st.progress(100) # set to original price

            bike_perc_resp = int((bike_resp_result/bike_org_price)*100)
            for percent_complete in range(bike_perc_resp):
                time.sleep(0.001)
                my_bar_bike.progress(percent_complete + 1)

            # For Average Price
            bike_resp_result2 = bike_response2.json()['bike_price_prediction']
            st.write('Average Price ', bike_resp_result2)
            bike_perc_resp2 = int((bike_resp_result2/bike_org_price)*100)
            bike_my_bar2 = st.progress(100) # set to original price

            for percent_complete in range(bike_perc_resp2):
                time.sleep(0.001)
                bike_my_bar2.progress(percent_complete + 1)
    with col2:
        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            else:
                return r.json()
        lottie_api = load_lottieurl('https://assets8.lottiefiles.com/packages/lf20_ztjvhpit.json')
        st_lottie(lottie_api, height=500, key='api')




if selected == 'Contact':
    st.header(':mailbox: Get In touch With Me!')

    # ---Contact Form---
    contact_form = """
    <form action="https://formsubmit.co/mnvsrinivas1@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    local_css("style/style.css")

    st.subheader('Follow me on')
    html = f"""<ul>
            <li style="display:inline-block;">
                <a href='{'https://www.linkedin.com/in/srinivas-menta-b96977214/'}'><img src='https://www.sfdcamplified.com/wp-content/uploads/2019/04/linkedin-logo-copy.png' width='25' height='25'></a>
            </li>
            <li style="display:inline-block;">
                <a href='{'https://github.com/Srinu2568'}'><img src='https://icones.pro/wp-content/uploads/2021/06/icone-github-bleu.png' width='25' height='25'></a>
            </li>
            <li style="display:inline-block;">
                <a href='{'https://www.instagram.com/mnv_srinivas/'}'><img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/2048px-Instagram_icon.png' width='25' height='25'></a>
            </li>
            <li style="display:inline-block;">
                <a href='{'https://medium.com/@mnvsrinivas1'}'><img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4tZSzY3tgMrgLEyJWY0fChWR-7gwDCHep0UEy_PE0sSiu_gUdXo6pM402iTW-jS4W0XY&usqp=CAU' width='25' height='25'></a>
            </li>
        </ul>"""
    # html = f"<a href='{'https://www.linkedin.com/in/srinivas-menta-b96977214/'}'><img src='https://www.sfdcamplified.com/wp-content/uploads/2019/04/linkedin-logo-copy.png' width='25' height='25'></a>"
    st.markdown(html, unsafe_allow_html=True)
    # 'https://png.pngtree.com/png-clipart/20180626/ourmid/pngtree-instagram-icon-instagram-logo-png-image_3584853.png'
