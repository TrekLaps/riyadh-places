#!/usr/bin/env python3
"""
Update places.json with category-matched Unsplash images.
Each category gets a curated pool of 15-25 VERIFIED working images that rotate.
ALL URLs verified via HTTP 200 check against Unsplash CDN.
"""

import json
import os
import subprocess

def url(photo_id):
    """Build Unsplash CDN URL from photo ID."""
    return f"https://images.unsplash.com/photo-{photo_id}?w=800&h=600&fit=crop&auto=format&q=80"

# ============================================================
# ALL IDs BELOW VERIFIED WITH HTTP 200 ✅
# ============================================================

CATEGORY_IMAGES = {
    # ==========================================
    # مطعم (Restaurants) - 580 places
    # ==========================================
    "مطعم": [
        url("1544025162-d76694265947"),  # grilled meat steak
        url("1555939594-58d7cb561ad1"),  # grilled food kebab
        url("1504674900247-0877df9cc836"),  # food plate beautiful
        url("1567620905732-2d1ec7ab7445"),  # food plate presentation
        url("1565299624946-b28f40a0ae38"),  # pizza food
        url("1540189549336-e6e99c3679fe"),  # salad fresh food
        url("1476224203421-9ac39bcb3327"),  # food dish restaurant
        url("1414235077428-338989a2e8c0"),  # fine dining plate
        url("1529694157872-4e0c0f3b238b"),  # steak close up
        url("1558030006-450675393462"),  # grilled ribs bbq
        url("1428515613728-6b4607e44363"),  # food plate variety
        url("1517248135467-4c7edcad34c4"),  # restaurant interior elegant
        url("1590846406792-0adc7f938f1d"),  # restaurant interior warm
        url("1466978913421-dad2ebd01d17"),  # restaurant outdoor patio
        url("1559339352-11d035aa65de"),  # restaurant night ambiance
        url("1552566626-52f8b828add9"),  # restaurant modern interior
        url("1537047902294-62a40c20a6ae"),  # food spread on table
        url("1600891964599-f61ba0e24092"),  # restaurant dish presentation
        url("1551218808-94e220e084d2"),  # restaurant bar area
        url("1578474846511-04ba529f0b88"),  # shawarma middle eastern
        url("1546069901-ba9599a7e63c"),  # food dish plated
        url("1574071318508-1cdbab80d002"),  # pasta dish restaurant
        url("1568901346375-23c9450c58cd"),  # food presentation elegant
        url("1484723091739-30a097e8f929"),  # restaurant bar cocktails
        url("1550547660-d9450f859349"),  # burger gourmet
    ],

    # ==========================================
    # كافيه (Cafes) - 350 places
    # ==========================================
    "كافيه": [
        url("1509042239860-f550ce710b93"),  # coffee cup beautiful
        url("1495474472287-4d71bcdd2085"),  # coffee latte art
        url("1442512595331-e89e73853f31"),  # coffee beans cup dark
        url("1501339847302-ac426a4a7cbb"),  # coffee shop interior cozy
        url("1453614512568-c4024d13c247"),  # coffee cup cafe morning
        url("1498804103079-a6351b050096"),  # coffee latte warm
        url("1461023058943-07fcbe16d735"),  # espresso coffee dark
        url("1511920170033-f8396924c348"),  # coffee making barista
        url("1559496417-e7f25cb247f3"),  # iced coffee refreshing
        url("1572442388796-11668a67e53d"),  # coffee pour action
        url("1554118811-1e0d58224f24"),  # cafe interior modern bright
        url("1521017432531-fbd92d768814"),  # cafe interior cozy warm
        url("1445116572660-236099ec97a0"),  # coffee shop ambiance
        url("1559925393-8be0ec4767c8"),  # cafe seating area
        url("1600093463592-8e36ae95ef56"),  # modern cafe design
        url("1493857671505-72967e2e2760"),  # cafe outdoor sidewalk
        url("1536935338788-846bb9981813"),  # matcha latte green
        url("1507133750040-4a8f57021571"),  # coffee beans raw
        url("1534040385115-33dcb3acba5b"),  # cafe window light
        url("1497935586351-b67a49e012bf"),  # coffee cup overhead view
        url("1485808191679-5f86510681a2"),  # coffee art barista
        url("1447933601403-0c6688de566e"),  # cafe interior with plants
        url("1497534446932-c925b458314e"),  # coffee cup close
        url("1504754524776-8f4f37790ca0"),  # coffee cup with steam
    ],

    # ==========================================
    # حلويات (Desserts) - 170 places
    # ==========================================
    "حلويات": [
        url("1551024601-bec78aea704b"),  # donuts colorful assorted
        url("1563729784474-d77dbb933a9e"),  # chocolate cake rich
        url("1488477181946-6428a0291777"),  # ice cream cones colorful
        url("1587314168485-3236d6710814"),  # baklava style pastry
        url("1578985545062-69928b1d9587"),  # chocolate cake beautiful
        url("1606313564200-e75d5e30476c"),  # pastries display case
        url("1558961363-fa8fdf82db35"),  # macarons assorted
        url("1551106652-a5bcf4b29ab6"),  # cheesecake slice
        url("1499636136210-6f4ee915583e"),  # cookies baking fresh
        url("1555244162-803834f70033"),  # ice cream scoop bowl
        url("1570145820259-b5b80c5c8bd6"),  # waffle dessert topping
        url("1464305795204-6f5bbfc7fb81"),  # cake slice elegant
        url("1612203985729-70726954388c"),  # turkish baklava kunafa
        url("1519915028121-7d3463d20b13"),  # pastries bakery display
        url("1586985289688-ca3cf47d3e6e"),  # croissant golden
        url("1495147466023-ac5c588e2e94"),  # ice cream cone summer
        url("1587668178277-295251f900ce"),  # tiramisu layered
        url("1560008581-09826d1de69e"),  # crepe dessert fruit
        url("1571115177098-24ec42ed204d"),  # donut frosted
        url("1562440499-64c9a111f713"),  # brownie chocolate rich
        url("1546039907-7fa05f864c02"),  # cupcake decorated
    ],

    # ==========================================
    # ترفيه (Entertainment) - 235 places
    # ==========================================
    "ترفيه": [
        url("1513151233558-d860c5398176"),  # fun confetti celebration
        url("1526512340740-9217d0159da9"),  # ferris wheel sunset
        url("1558008258-3256797b43f3"),  # laser neon lights
        url("1511882150382-421056c89033"),  # gaming controller
        url("1560419015-7c427e8ae5ba"),  # VR headset virtual reality
        url("1478720568477-152d9b164e26"),  # cinema movie theater
        url("1559223607-a43c990c692c"),  # roller coaster ride
        url("1569863959165-56dae551d4fc"),  # trampoline park jump
        url("1534423861386-85a16f5d13fd"),  # neon lights colorful
        url("1585951237318-9ea5e175b891"),  # escape room puzzle
        url("1518709766631-a6a7f45921c3"),  # movie night popcorn
        url("1614680376593-902f74cf0d41"),  # arcade neon gaming
        url("1576485290814-1c72aa4bbb8e"),  # billiards pool table
        url("1596461404969-9ae70f2830c1"),  # laser tag fun
        url("1560986752-2e31d9507413"),  # waterpark splash fun
        url("1519389950473-47ba0277781c"),  # family fun time
        url("1470225620780-dba8ba36b745"),  # DJ music party
        url("1536440136628-849c177e76a1"),  # movie screen cinema
        url("1574629810360-7efbbe195018"),  # outdoor activity fun
        url("1493711662062-fa541adb3fc8"),  # concert fun excitement
    ],

    # ==========================================
    # طبيعة (Nature) - 130 places
    # ==========================================
    "طبيعة": [
        url("1507525428034-b723cf961d3e"),  # beach scenic tropical
        url("1441974231531-c6227db76b6e"),  # forest green lush
        url("1501785888041-af3ef285b470"),  # mountain lake scenic
        url("1506744038136-46273834b3fb"),  # landscape mountain valley
        url("1469474968028-56623f02e42e"),  # sunset landscape golden
        url("1418065460487-3e41a6c84dc5"),  # forest trees sunlight
        url("1472214103451-9374bd1c798e"),  # green valley nature
        url("1504280390367-361c6d9f38f4"),  # camping tent outdoor
        url("1510312305653-8ed496efae75"),  # starry night desert sky
        url("1473580044384-7ba9967e16a0"),  # desert sand dunes
        url("1509316975850-ff9c5deb0cd9"),  # sunset desert golden
        url("1547036967-23d11aacaee0"),  # sand dunes pattern
        url("1449824913935-59a10b8d2000"),  # oasis palm trees water
        url("1433086966358-54859d0ed716"),  # waterfall nature
        url("1470071459604-3b5ec3a7fe05"),  # countryside green fields
        url("1500534314209-a25ddb2bd429"),  # green park trees
        url("1464822759023-fed622ff2c3b"),  # mountain landscape
        url("1545389336-cf090694435e"),  # canyon desert rocks
        url("1528184039930-bd03972bd974"),  # desert road sunset
        url("1489710437720-ebb67ec84dd2"),  # palm trees tropical
        url("1543002588-bfa74002ed7e"),  # sunset desert scenic
    ],

    # ==========================================
    # تسوق (Shopping) - 125 places
    # ==========================================
    "تسوق": [
        url("1441986300917-64674bd600d8"),  # clothing store interior
        url("1555529669-e69e7aa0ba9a"),  # shopping bags colorful
        url("1472851294608-062f824d29cc"),  # boutique store front
        url("1483985988355-763728e1935b"),  # women shopping fashion
        url("1556742049-0cfed4f6a45d"),  # electronics store tech
        url("1534723452862-4c874018d66d"),  # market bazaar traditional
        url("1567401893414-76b7b1e5a7a5"),  # clothing rack fashion
        url("1441984904996-e0b6ba687e04"),  # fashion store interior
        url("1604719312566-8912e9227c6a"),  # luxury brand store
        url("1607082349566-187342175e2f"),  # shopping cart experience
        url("1526045612212-70caf35c14df"),  # watches jewelry luxury
        url("1570857502809-08184874388e"),  # traditional market scene
        url("1590874103328-eac38a683ce7"),  # gift shop display
        url("1600185365926-3a2ce3cdb9eb"),  # sneakers shoes display
        url("1582738411706-bfc8e691d1c2"),  # makeup cosmetics beauty
        url("1583922606661-0822ed0bd916"),  # oud perfume arabic
        url("1556742111-a301076d9d18"),  # grocery market fresh
        url("1560243563-062bfc001d68"),  # bookstore shelves
        url("1586880244386-8b3e34c8382c"),  # flower shop colorful
        url("1566665797739-1674de7a421a"),  # shopping street
    ],

    # ==========================================
    # شاليه (Chalets) - 120 places
    # ==========================================
    "شاليه": [
        url("1571003123894-1f0594d2b5d9"),  # luxury house exterior
        url("1600585154340-be6161a56a0c"),  # beautiful home exterior
        url("1600596542815-ffad4c1539a9"),  # modern house exterior
        url("1575517111478-7f6afd0973db"),  # swimming pool overhead
        url("1499793983690-e29da59ef1c2"),  # beach house villa
        url("1512917774080-9991f1c4c750"),  # luxury villa exterior
        url("1613977257363-707ba9348227"),  # pool villa night
        url("1540518614846-7eded433c457"),  # luxury bedroom elegant
        url("1582268611958-ebfd161ef9cf"),  # modern villa design
        url("1560448204-e02f11c3d0e2"),  # hotel room luxury view
        url("1564013799919-ab600027ffc6"),  # modern dream house
        url("1580587771525-78b9dba3b914"),  # luxury home beautiful
        url("1600607687939-ce8a6c25118c"),  # pool area resort
        url("1600047509807-ba8f99d2cdde"),  # modern backyard pool
        url("1583608205776-bfd35f0d9f83"),  # villa exterior modern
        url("1613545325268-9265e1609167"),  # luxury pool area
        url("1600566753086-00f18fb6b3ea"),  # interior living room
        url("1600210492486-724fe5c67fb0"),  # modern kitchen luxury
        url("1579783902614-a3fb3927b6a5"),  # resort swimming pool
        url("1570129477492-45c003edd2be"),  # villa terrace view
    ],

    # ==========================================
    # فنادق (Hotels) - 120 places
    # ==========================================
    "فنادق": [
        url("1566073771259-6a8506099945"),  # hotel resort pool
        url("1551882547-ff40c63fe5fa"),  # hotel building exterior
        url("1520250497591-112f2f40a3f4"),  # resort hotel pool
        url("1542314831-068cd1dbfeeb"),  # hotel lobby interior
        url("1455587734955-081b22074882"),  # luxury hotel pool
        url("1564501049412-61c2a3083791"),  # hotel room modern
        url("1445019980597-93fa8acb246c"),  # hotel room bed
        url("1582719508461-905c673771fd"),  # luxury hotel building
        url("1578683010236-d716f9a3f461"),  # luxury room interior
        url("1584132967334-10e028bd69f7"),  # hotel bathroom
        url("1568084680786-a84f91d1153c"),  # hotel infinity pool
        url("1590490360182-c33d57733427"),  # hotel room view
        url("1571896349842-33c89424de2d"),  # hotel facade
        url("1519449556851-5720b33024e7"),  # hotel dining luxury
        url("1596394516093-501ba68a0ba6"),  # luxury hotel room
        url("1551632436-cbf8dd35adfa"),  # hotel pool tropical
        url("1563911892437-1feda0179e1b"),  # hotel reception desk
        url("1611892440504-42a792e24d32"),  # luxury suite room
        url("1549294413-26f195200c16"),  # hotel hallway elegant
        url("1578645510447-e20b4311e3ce"),  # modern hotel design
    ],

    # ==========================================
    # مولات (Malls) - 50 places
    # ==========================================
    "مولات": [
        url("1519566335946-e6f65f0f4fdf"),  # shopping mall interior
        url("1441986300917-64674bd600d8"),  # store in mall
        url("1472851294608-062f824d29cc"),  # boutique mall
        url("1556742049-0cfed4f6a45d"),  # electronics section
        url("1483985988355-763728e1935b"),  # shoppers in mall
        url("1604719312566-8912e9227c6a"),  # luxury brand store
        url("1441984904996-e0b6ba687e04"),  # fashion store mall
        url("1567401893414-76b7b1e5a7a5"),  # clothing display
        url("1607082349566-187342175e2f"),  # shopping experience
        url("1555529669-e69e7aa0ba9a"),  # shopping bags
        url("1526045612212-70caf35c14df"),  # luxury watch display
        url("1560243563-062bfc001d68"),  # bookstore in mall
        url("1606567595334-d39972c85dbe"),  # mall entrance modern
        url("1566665797739-1674de7a421a"),  # shopping district
        url("1534723452862-4c874018d66d"),  # market area
    ],

    # ==========================================
    # متاحف (Museums) - 60 places
    # ==========================================
    "متاحف": [
        url("1572953109213-3be62398eb95"),  # museum exhibit modern
        url("1554907984-15263bfd63bd"),  # art gallery white
        url("1518998053901-5348d3961a04"),  # modern art installation
        url("1513364776144-60967b0f800f"),  # art painting colorful
        url("1531243269054-5ebf6f34081e"),  # museum hall grand
        url("1544967082-d9d25d867d66"),  # cultural exhibit
        url("1574182245530-967d9b3831af"),  # museum corridor
        url("1566127444979-b3d2b654e3d7"),  # art gallery modern
        url("1527090526205-beaac8dc3c62"),  # museum architecture
        url("1547891654-e66ed7ebb968"),  # abstract art modern
        url("1568702846914-96b305d2aaeb"),  # sculpture modern
        url("1541367777708-7905fe3296c0"),  # museum display
        url("1582555172866-f73bb12a2ab3"),  # art exhibition
        url("1578662996442-48f60103fc96"),  # art piece modern
        url("1507003211169-0a1dd7228f2d"),  # portrait in gallery
    ],

    # ==========================================
    # فعاليات (Events) - 60 places
    # ==========================================
    "فعاليات": [
        url("1540575467063-178a50c2df87"),  # conference event
        url("1492684223066-81342ee5ff30"),  # festival crowd lights
        url("1501281668745-f7f57925c3b4"),  # crowd concert
        url("1514525253161-7a46d19cd819"),  # concert performance
        url("1505373877841-8d25f7d46678"),  # tech conference
        url("1560439514-4e9645039924"),  # exhibition hall
        url("1429962714451-bb934ecdc4ec"),  # dj concert night
        url("1531058020387-3be344556be6"),  # outdoor event party
        url("1475721027785-f74eccf877e2"),  # speaker event
        url("1459749411175-04bf5292ceea"),  # concert lights stage
        url("1533174072545-7a4b6ad7a6c3"),  # party celebration
        url("1478147427282-58a87a120781"),  # event crowd audience
        url("1524368535928-5b5e00ddc76b"),  # fireworks celebration
        url("1540747913346-19e32dc3e97e"),  # tech conference hall
        url("1470229722913-7c0e2dbbafd3"),  # music festival
        url("1528569937393-ee892b976859"),  # fireworks night sky
        url("1508193638397-1c4234db14d8"),  # DJ concert performance
    ],
}


def update_places():
    """Update places.json with category-matched images."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    places_file = os.path.join(data_dir, 'places.json')
    
    print(f"Reading {places_file}...")
    with open(places_file, 'r', encoding='utf-8') as f:
        places = json.load(f)
    
    print(f"Total places: {len(places)}")
    
    # Track per-category counters for rotation
    category_counters = {}
    updated_count = 0
    category_stats = {}
    
    for place in places:
        category = place.get('category', '')
        
        if category not in CATEGORY_IMAGES:
            print(f"WARNING: Unknown category '{category}' for place '{place.get('name_en', 'unknown')}'")
            continue
        
        pool = CATEGORY_IMAGES[category]
        if not pool:
            continue
        
        if category not in category_counters:
            category_counters[category] = 0
            category_stats[category] = 0
        
        idx = category_counters[category] % len(pool)
        place['image_url'] = pool[idx]
        
        category_counters[category] += 1
        category_stats[category] += 1
        updated_count += 1
    
    print(f"\nUpdated {updated_count} places:")
    for cat, count in sorted(category_stats.items(), key=lambda x: -x[1]):
        pool_size = len(CATEGORY_IMAGES.get(cat, []))
        print(f"  {cat}: {count} places rotating through {pool_size} images")
    
    # Write back
    print(f"\nWriting {places_file}...")
    with open(places_file, 'w', encoding='utf-8') as f:
        json.dump(places, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Done! Updated {updated_count} places with category-matched images.")
    return updated_count


if __name__ == '__main__':
    update_places()
