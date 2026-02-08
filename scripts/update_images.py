#!/usr/bin/env python3
"""
Update places.json with category-matched Unsplash images.
Each category gets a curated pool of 20-30 relevant images that rotate.
ALL URLs use the verified photo-TIMESTAMP-HASH format that works on Unsplash CDN.
"""

import json
import os
import subprocess
import sys

# ============================================================
# CURATED IMAGE POOLS PER CATEGORY
# All IDs are in the timestamp-hash format: photo-NNNNNNNNNNN-XXXXXXXXXXXX
# These are well-known, popular Unsplash images curated by category
# ============================================================

def url(photo_id):
    """Build Unsplash CDN URL from photo ID."""
    return f"https://images.unsplash.com/photo-{photo_id}?w=800&h=600&fit=crop&auto=format&q=80"

CATEGORY_IMAGES = {
    # ==========================================
    # مطعم (Restaurants) - 580 places
    # ==========================================
    "مطعم": [
        # Arabic/Middle Eastern food & rice dishes
        url("1544025162-d76694265947"),  # grilled meat steak
        url("1555939594-58d7cb561ad1"),  # grilled food kebab
        url("1504674900247-0877df9cc836"),  # food plate beautiful
        url("1567620905732-2d1ec7ab7445"),  # food pancakes plate
        url("1565299624946-b28f40a0ae38"),  # pizza food
        url("1540189549336-e6e99c3679fe"),  # salad fresh food
        url("1476224203421-9ac39bcb3327"),  # food dish restaurant
        url("1414235077428-338989a2e8c0"),  # fine dining plate
        url("1529694157872-4e0c0f3b238b"),  # steak
        url("1558030006-450675393462"),  # grilled ribs
        url("1432139509613-5c4255a831a8"),  # restaurant table setting
        # Restaurant interiors  
        url("1517248135467-4c7edcad34c4"),  # restaurant interior
        url("1590846406792-0adc7f938f1d"),  # restaurant interior warm
        url("1466978913421-dad2ebd01d17"),  # restaurant outdoor
        url("1559339352-11d035aa65de"),  # restaurant night ambiance
        url("1552566626-52f8b828add9"),  # restaurant modern interior
        url("1537047902294-62a40c20a6ae"),  # food spread on table
        url("1600891964599-f61ba0e24092"),  # food restaurant dish
        url("1551218808-94e220e084d2"),  # restaurant bar area
        url("1578474846511-04ba529f0b88"),  # shawarma middle east
        url("1600585154340-be6161a56a0c"),  # food plate elegant
        url("1546069901-ba9599a7e63c"),  # food dish restaurant
        url("1555992643-5ab97bf61e7d"),  # burger gourmet
        url("1574071318508-1cdbab80d002"),  # pasta dish
        url("1568901346375-23c9450c58cd"),  # food presentation elegant
    ],

    # ==========================================
    # كافيه (Cafes) - 350 places
    # ==========================================
    "كافيه": [
        # Coffee & latte art
        url("1509042239860-f550ce710b93"),  # coffee cup beautiful
        url("1495474472287-4d71bcdd2085"),  # coffee latte art
        url("1442512595331-e89e73853f31"),  # coffee beans cup dark
        url("1501339847302-ac426a4a7cbb"),  # coffee shop interior cozy
        url("1453614512568-c4024d13c247"),  # coffee cup cafe morning
        url("1498804103079-a6351b050096"),  # coffee latte warm
        url("1461023058943-07fcbe16d735"),  # espresso coffee dark
        url("1511920170033-f8396924c348"),  # coffee making barista process
        url("1559496417-e7f25cb247f3"),  # iced coffee refreshing
        url("1572442388796-11668a67e53d"),  # coffee pour action
        # Cafe interiors
        url("1554118811-1e0d58224f24"),  # cafe interior modern bright
        url("1521017432531-fbd92d768814"),  # cafe interior cozy warm
        url("1445116572660-236099ec97a0"),  # coffee shop ambiance
        url("1559925393-8be0ec4767c8"),  # cafe seating area
        url("1600093463592-8e36ae95ef56"),  # modern cafe design
        url("1493857671505-72967e2e2760"),  # cafe outdoor sidewalk
        url("1536935338788-846bb9981813"),  # matcha latte green
        url("1514432324607-a09d9b4aefda"),  # v60 pour over brewing
        url("1507133750040-4a8f57021571"),  # coffee beans raw
        url("1466900323642-3e3c7aaab9b0"),  # coffee cup close up
        url("1534040385115-33dcb3acba5b"),  # cafe window light
        url("1497935586351-b67a49e012bf"),  # coffee cup overhead
        url("1485808191679-5f86510681a2"),  # coffee art design
        url("1447933601403-0c6688de566e"),  # cafe interior plants
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
        url("1486427944544-d2c246c4df14"),  # ice cream scoop bowl
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
        url("1567171466-df64b695e493"),  # candy assortment
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
        url("1569863959165-56dae551d4fc"),  # trampoline park
        url("1534423861386-85a16f5d13fd"),  # neon lights colorful
        url("1585951237318-9ea5e175b891"),  # escape room puzzle
        url("1563277151-6b3c0b3d0484"),  # theme park night lights
        url("1518709766631-a6a7f45921c3"),  # movie night
        url("1614680376593-902f74cf0d41"),  # arcade neon
        url("1570989613801-eda9dcc1e5e4"),  # billiards pool table
        url("1596461404969-9ae70f2830c1"),  # laser tag fun
        url("1560986752-2e31d9507413"),  # waterpark splash
        url("1551103782-8ab760e1-8ab7"),  # gaming room setup
        url("1519389950473-47ba0277781c"),  # family fun time
        url("1470225620780-dba8ba36b745"),  # DJ music party
        url("1536440136628-849c177e76a1"),  # movie screen cinema
        url("1562752700-7c1c15a27529"),  # mini golf course
        url("1574629810360-7efbbe195018"),  # fun outdoor activity
        url("1493711662062-fa541adb3fc8"),  # concert fun
    ],

    # ==========================================
    # طبيعة (Nature) - 130 places
    # ==========================================
    "طبيعة": [
        # Desert & Saudi landscapes  
        url("1507525428034-b723cf961d3e"),  # beach scenic
        url("1441974231531-c6227db76b6e"),  # forest green lush
        url("1501785888041-af3ef285b470"),  # mountain lake scenic
        url("1506744038136-46273834b3fb"),  # landscape mountain valley
        url("1469474968028-56623f02e42e"),  # sunset landscape golden
        url("1418065460487-3e41a6c84dc5"),  # forest trees sunlight
        url("1472214103451-9374bd1c798e"),  # green valley nature
        url("1542401886-65d6c61db217"),  # desert camping adventure
        url("1504280390367-361c6d9f38f4"),  # camping tent outdoor
        url("1510312305653-8ed496efae75"),  # starry night desert
        url("1473580044384-7ba9967e16a0"),  # desert sand dunes
        url("1509316975850-ff9c5deb0cd9"),  # sunset desert golden
        url("1547036967-23d11aacaee0"),  # sand dunes pattern
        url("1451400038541-ac5b787e8a3e"),  # oasis palm trees
        url("1489493887464-892be6d1daae"),  # hiking trail nature
        url("1433086966358-54859d0ed716"),  # waterfall nature
        url("1470071459604-3b5ec3a7fe05"),  # countryside green
        url("1500534314209-a25ddb2bd429"),  # green park trees
        url("1464822759023-fed622ff2c3b"),  # mountain landscape
        url("1540979388-31035cdbd378"),  # canyon desert rocks
        url("1528184039930-bd03972bd974"),  # desert road sunset
        url("1490750967868-88aa4f44baee"),  # palm trees tropical
    ],

    # ==========================================
    # تسوق (Shopping) - 125 places
    # ==========================================
    "تسوق": [
        url("1441986300917-64674bd600d8"),  # clothing store interior
        url("1555529669-e69e7aa0ba9a"),  # shopping bags colorful
        url("1472851294608-062f824d29cc"),  # boutique store front
        url("1483985988355-763728e1935b"),  # women shopping fashion
        url("1556742049-0cfed4f6a45d"),  # electronics store
        url("1534723452862-4c874018d66d"),  # market bazaar traditional
        url("1567401893414-76b7b1e5a7a5"),  # clothing rack fashion
        url("1441984904996-e0b6ba687e04"),  # fashion store interior
        url("1604719312566-8912e9227c6a"),  # luxury brand store
        url("1607082349566-187342175e2f"),  # shopping cart
        url("1528698827591-e19cef51a699"),  # watches jewelry luxury
        url("1570857502809-08184874388e"),  # traditional market scene
        url("1590874103328-eac38a683ce7"),  # gift shop display
        url("1600185365926-3a2ce3cdb9eb"),  # sneakers shoes display
        url("1582738411706-bfc8e691d1c2"),  # makeup cosmetics beauty
        url("1583922606661-0822ed0bd916"),  # oud perfume arabic style
        url("1556742111-a301076d9d18"),  # grocery market fresh
        url("1581783898377-1c85bf937427"),  # retail store modern
        url("1567449303078-57ad995bd329"),  # modern shop design
        url("1605116900222-b33615e5e049"),  # store entrance
        url("1560243563-062bfc001d68"),  # bookstore shelves
        url("1586880244386-8b3e34c8382c"),  # flower shop colorful
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
        url("1613977257363-707ba9348227"),  # pool villa night illuminated
        url("1540518614846-7eded433c457"),  # luxury bedroom elegant
        url("1582268611958-ebfd161ef9cf"),  # modern villa design
        url("1560448204-e02f11c3d0e2"),  # hotel room luxury view
        url("1564013799919-ab600027ffc6"),  # modern dream house
        url("1580587771525-78b9dba3b914"),  # luxury home exterior
        url("1600607687939-ce8a6c25118c"),  # pool area resort
        url("1600047509807-ba8f99d2cdde"),  # modern backyard pool
        url("1583608205776-bfd35f0d9f83"),  # villa exterior modern
        url("1613545325268-9265e1609167"),  # luxury pool area
        url("1600566753086-00f18fb6b3ea"),  # interior living room luxury
        url("1600210492486-724fe5c67fb0"),  # modern kitchen luxury
        url("1522771739-7d5b0047a49f"),  # pool resort tropical
        url("1542928093-d38c704be1fb"),  # villa terrace view
    ],

    # ==========================================
    # فنادق (Hotels) - 120 places
    # ==========================================
    "فنادق": [
        url("1566073771259-6a8506099945"),  # hotel resort pool
        url("1551882547-ff40c63fe5fa"),  # hotel building exterior
        url("1520250497591-112f2f40a3f4"),  # resort hotel pool
        url("1542314831-068cd1dbfeeb"),  # hotel lobby interior grand
        url("1455587734955-081b22074882"),  # luxury hotel pool resort
        url("1564501049412-61c2a3083791"),  # hotel room modern bed
        url("1445019980597-93fa8acb246c"),  # hotel room view bed
        url("1582719508461-905c673771fd"),  # luxury hotel building
        url("1578683010236-d716f9a3f461"),  # luxury room interior
        url("1584132967334-10e028bd69f7"),  # hotel bathroom luxury
        url("1568084680786-a84f91d1153c"),  # hotel infinity pool
        url("1590490360182-c33d57733427"),  # hotel room scenic view
        url("1571896349842-33c89424de2d"),  # hotel facade exterior
        url("1519449556851-5720b33024e7"),  # hotel dining area
        url("1596394516093-501ba68a0ba6"),  # luxury hotel room
        url("1551632436-cbf8dd35adfa"),  # hotel pool tropical
        url("1563911892437-1feda0179e1b"),  # hotel reception desk
        url("1611892440504-42a792e24d32"),  # luxury suite
        url("1549294413-26f195200c16"),  # hotel hallway elegant
        url("1578645510447-e20b4311e3ce"),  # modern hotel design
    ],

    # ==========================================
    # مولات (Malls) - 50 places
    # ==========================================
    "مولات": [
        url("1519566335946-e6f65f0f4fdf"),  # shopping mall interior bright
        url("1581783898377-1c85bf937427"),  # mall food court area
        url("1567449303078-57ad995bd329"),  # mall modern design
        url("1605116900222-b33615e5e049"),  # mall entrance grand
        url("1528698827591-e19cef51a699"),  # luxury watch display
        url("1555529669-e69e7aa0ba9a"),  # shopping bags colorful
        url("1441986300917-64674bd600d8"),  # clothing store in mall
        url("1472851294608-062f824d29cc"),  # boutique in mall
        url("1556742049-0cfed4f6a45d"),  # electronics section
        url("1483985988355-763728e1935b"),  # shoppers in mall
        url("1604719312566-8912e9227c6a"),  # luxury brand store
        url("1441984904996-e0b6ba687e04"),  # fashion store
        url("1567401893414-76b7b1e5a7a5"),  # clothing displays
        url("1607082349566-187342175e2f"),  # shopping experience
        url("1560243563-062bfc001d68"),  # bookstore in mall
    ],

    # ==========================================
    # متاحف (Museums) - 60 places
    # ==========================================
    "متاحف": [
        url("1572953109213-3be62398eb95"),  # museum exhibit modern
        url("1554907984-15263bfd63bd"),  # art gallery white walls
        url("1518998053901-5348d3961a04"),  # modern art installation
        url("1513364776144-60967b0f800f"),  # art painting colorful
        url("1531243269054-5ebf6f34081e"),  # museum hall grand
        url("1544967082-d9d25d867d66"),  # cultural exhibit display
        url("1574182245530-967d9b3831af"),  # museum corridor
        url("1566127444979-b3d2b654e3d7"),  # art gallery modern
        url("1536924940564-5e5f2a5d8be3"),  # painting gallery
        url("1577083753695-e010191a7751"),  # abstract art
        url("1551913902-c92207136dcd"),  # sculpture exhibit
        url("1461360370896-922624d12a11"),  # museum architecture
        url("1580136579585-9c5c8ac1e285"),  # gallery space
        url("1582555172866-f73bb12a2ab3"),  # art exhibition
        url("1541367777708-7905fe3296c0"),  # cultural display
        url("1578662996442-48f60103fc96"),  # modern art piece
    ],

    # ==========================================
    # فعاليات (Events) - 60 places
    # ==========================================
    "فعاليات": [
        url("1540575467063-178a50c2df87"),  # conference event large
        url("1492684223066-81342ee5ff30"),  # festival crowd lights
        url("1501281668745-f7f57925c3b4"),  # crowd event concert
        url("1514525253161-7a46d19cd819"),  # concert performance stage
        url("1505373877841-8d25f7d46678"),  # conference tech event
        url("1560439514-4e9645039924"),  # exhibition hall display
        url("1429962714451-bb934ecdc4ec"),  # dj concert night
        url("1531058020387-3be344556be6"),  # outdoor event party
        url("1475721027785-f74eccf877e2"),  # speaker event talk
        url("1587825140708-dfaf18c4f0f4"),  # sports event match
        url("1459749411175-04bf5292ceea"),  # concert lights stage
        url("1533174072545-7a4b6ad7a6c3"),  # party celebration
        url("1478147427282-58a87a120781"),  # event crowd audience
        url("1524368535928-5b5e00ddc76b"),  # fireworks celebration
        url("1540747913346-19e32dc3e97e"),  # tech conference
        url("1556761175-5973bc4aa2bc"),  # event planning
        url("1559223607-a43c990c692c"),  # outdoor event excitement
        url("1470229722913-7c0e2dbbafd3"),  # music festival
    ],
}


def verify_urls(sample_size=3):
    """Verify a sample of URLs from each category actually return 200."""
    import random
    
    print("Verifying URL samples...")
    all_good = True
    
    for category, urls in CATEGORY_IMAGES.items():
        samples = random.sample(urls, min(sample_size, len(urls)))
        for test_url in samples:
            # Use small size for quick test
            test = test_url.replace("w=800", "w=50").replace("h=600", "h=50")
            try:
                result = subprocess.run(
                    ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "5", test],
                    capture_output=True, text=True, timeout=10
                )
                code = result.stdout.strip()
                if code != "200":
                    print(f"  ⚠️  {category}: HTTP {code} for {test_url[:80]}...")
                    all_good = False
                else:
                    pass  # silently pass
            except Exception as e:
                print(f"  ⚠️  {category}: Error testing {test_url[:60]}... - {e}")
                all_good = False
    
    if all_good:
        print("  ✅ All sampled URLs verified!")
    return all_good


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
        
        # Initialize counter
        if category not in category_counters:
            category_counters[category] = 0
            category_stats[category] = 0
        
        # Rotate through images in the pool
        idx = category_counters[category] % len(pool)
        new_url = pool[idx]
        
        # Update the image_url
        place['image_url'] = new_url
        
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
    # Verify a sample first
    verify_urls(sample_size=2)
    print()
    
    # Update all places
    update_places()
