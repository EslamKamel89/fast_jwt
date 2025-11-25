from __future__ import annotations

import asyncio
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.sandbox.models import (Category, Order, OrderItem, Product,
                                     Profile)
from app.apps.users.models import User
from app.core.security import Security
from app.db.session import AsyncSessionLocal  # your async_sessionmaker

USERS = [
    {"name":"Alice Johnson","email":"alice.johnson@example.com","password":"Password123!","role":"user"},
    {"name":"Bob Williams","email":"bob.williams@example.com","password":"Password123!","role":"user"},
    {"name":"Carol Smith","email":"carol.smith@example.com","password":"Password123!","role":"admin"},
    {"name":"David Brown","email":"david.brown@example.com","password":"Password123!","role":"user"},
    {"name":"Emily Davis","email":"emily.davis@example.com","password":"Password123!","role":"user"},
    {"name":"Frank Miller","email":"frank.miller@example.com","password":"Password123!","role":"user"},
    {"name":"Grace Wilson","email":"grace.wilson@example.com","password":"Password123!","role":"user"},
    {"name":"Henry Moore","email":"henry.moore@example.com","password":"Password123!","role":"user"},
    {"name":"Isabella Taylor","email":"isabella.taylor@example.com","password":"Password123!","role":"user"},
    {"name":"Jack Anderson","email":"jack.anderson@example.com","password":"Password123!","role":"admin"},
    {"name":"Karen Thomas","email":"karen.thomas@example.com","password":"Password123!","role":"user"},
    {"name":"Liam Jackson","email":"liam.jackson@example.com","password":"Password123!","role":"user"},
    {"name":"Mia White","email":"mia.white@example.com","password":"Password123!","role":"user"},
    {"name":"Noah Harris","email":"noah.harris@example.com","password":"Password123!","role":"user"},
    {"name":"Olivia Martin","email":"olivia.martin@example.com","password":"Password123!","role":"user"},
    {"name":"Paul Thompson","email":"paul.thompson@example.com","password":"Password123!","role":"user"},
    {"name":"Quinn Garcia","email":"quinn.garcia@example.com","password":"Password123!","role":"user"},
    {"name":"Rachel Martinez","email":"rachel.martinez@example.com","password":"Password123!","role":"user"},
    {"name":"Samuel Robinson","email":"samuel.robinson@example.com","password":"Password123!","role":"user"},
    {"name":"Tina Clark","email":"tina.clark@example.com","password":"Password123!","role":"user"},
    {"name":"Umar Rodriguez","email":"umar.rodriguez@example.com","password":"Password123!","role":"user"},
    {"name":"Vera Lewis","email":"vera.lewis@example.com","password":"Password123!","role":"user"},
    {"name":"Will Young","email":"will.young@example.com","password":"Password123!","role":"admin"},
    {"name":"Xavier King","email":"xavier.king@example.com","password":"Password123!","role":"user"},
    {"name":"Yara Wright","email":"yara.wright@example.com","password":"Password123!","role":"user"},
    {"name":"Zoe Lopez","email":"zoe.lopez@example.com","password":"Password123!","role":"user"},
    {"name":"Aaron Hill","email":"aaron.hill@example.com","password":"Password123!","role":"user"},
    {"name":"Beth Green","email":"beth.green@example.com","password":"Password123!","role":"user"},
    {"name":"Cody Adams","email":"cody.adams@example.com","password":"Password123!","role":"user"},
    {"name":"Diana Baker","email":"diana.baker@example.com","password":"Password123!","role":"user"},
    {"name":"Ethan Nelson","email":"ethan.nelson@example.com","password":"Password123!","role":"user"},
    {"name":"Fiona Carter","email":"fiona.carter@example.com","password":"Password123!","role":"user"},
    {"name":"Gabe Mitchell","email":"gabe.mitchell@example.com","password":"Password123!","role":"user"},
    {"name":"Hannah Perez","email":"hannah.perez@example.com","password":"Password123!","role":"user"},
    {"name":"Ian Roberts","email":"ian.roberts@example.com","password":"Password123!","role":"user"},
    {"name":"Jade Turner","email":"jade.turner@example.com","password":"Password123!","role":"user"},
    {"name":"Kyle Phillips","email":"kyle.phillips@example.com","password":"Password123!","role":"user"},
    {"name":"Lara Campbell","email":"lara.campbell@example.com","password":"Password123!","role":"user"},
    {"name":"Mason Parker","email":"mason.parker@example.com","password":"Password123!","role":"user"},
    {"name":"Nina Evans","email":"nina.evans@example.com","password":"Password123!","role":"user"},
    {"name":"Owen Edwards","email":"owen.edwards@example.com","password":"Password123!","role":"user"},
    {"name":"Piper Collins","email":"piper.collins@example.com","password":"Password123!","role":"user"},
    {"name":"Quincy Stewart","email":"quincy.stewart@example.com","password":"Password123!","role":"user"},
    {"name":"Rita Sanchez","email":"rita.sanchez@example.com","password":"Password123!","role":"user"},
    {"name":"Sean Morris","email":"sean.morris@example.com","password":"Password123!","role":"user"},
    {"name":"Tara Rogers","email":"tara.rogers@example.com","password":"Password123!","role":"user"},
    {"name":"Usha Reed","email":"usha.reed@example.com","password":"Password123!","role":"user"},
    {"name":"Victor Cook","email":"victor.cook@example.com","password":"Password123!","role":"user"},
    {"name":"Wendy Morgan","email":"wendy.morgan@example.com","password":"Password123!","role":"user"},
    {"name":"Xena Bell","email":"xena.bell@example.com","password":"Password123!","role":"user"},
    {"name":"Yosef Bailey","email":"yosef.bailey@example.com","password":"Password123!","role":"user"},
    {"name":"Zara Rivera","email":"zara.rivera@example.com","password":"Password123!","role":"user"},
    {"name":"Alan Foster","email":"alan.foster@example.com","password":"Password123!","role":"user"},
    {"name":"Bianca Gonzales","email":"bianca.gonzales@example.com","password":"Password123!","role":"user"},
]

PRODUCTS: list[dict[str , str|float]] = [
    {"name":"Apple iPhone 14 Pro Max","price":1099.00},
    {"name":"Samsung Galaxy S23 Ultra","price":1199.00},
    {"name":"Google Pixel 7 Pro","price":899.00},
    {"name":"Sony WH-1000XM5 Headphones","price":399.99},
    {"name":"Apple AirPods Pro (2nd gen)","price":249.00},
    {"name":"Samsung Galaxy Buds2 Pro","price":199.99},
    {"name":"Bose QuietComfort Earbuds","price":279.00},
    {"name":"Apple Watch Series 9","price":399.00},
    {"name":"Fitbit Charge 5","price":149.95},
    {"name":"Garmin Forerunner 265","price":349.99},
    {"name":"Dell XPS 13 Laptop","price":999.99},
    {"name":"MacBook Air M2 13-inch","price":1199.00},
    {"name":"MacBook Pro 14-inch M2 Pro","price":1999.00},
    {"name":"Lenovo ThinkPad X1 Carbon","price":1299.00},
    {"name":"ASUS ROG Strix G16 Gaming Laptop","price":1499.99},
    {"name":"Apple iPad Air","price":599.00},
    {"name":"Samsung Galaxy Tab S8","price":699.99},
    {"name":"Amazon Kindle Paperwhite","price":139.99},
    {"name":"Logitech MX Master 3 Mouse","price":99.99},
    {"name":"Razer DeathAdder V3 Pro Mouse","price":129.99},
    {"name":"Keychron K2 Mechanical Keyboard","price":89.99},
    {"name":"Corsair K70 RGB Keyboard","price":149.99},
    {"name":"Anker 65W USB-C Charger","price":39.99},
    {"name":"Belkin Wireless Charger 15W","price":29.99},
    {"name":"SanDisk Extreme 1TB SSD","price":109.99},
    {"name":"Western Digital 4TB HDD","price":89.99},
    {"name":"Seagate Portable 2TB HDD","price":69.99},
    {"name":"Canon EOS R10 Mirrorless Camera","price":979.00},
    {"name":"Nikon Z50 Mirrorless Camera","price":849.00},
    {"name":"GoPro HERO11 Black","price":399.99},
    {"name":"DJI Mini 4 Drone","price":499.00},
    {"name":"Philips Hue Starter Kit (3 bulbs)","price":179.99},
    {"name":"Google Nest Thermostat","price":129.00},
    {"name":"Ring Video Doorbell Pro","price":199.99},
    {"name":"Arlo Pro 4 Security Camera","price":299.99},
    {"name":"Sony PlayStation 5 Console","price":499.99},
    {"name":"Microsoft Xbox Series X","price":499.99},
    {"name":"Nintendo Switch OLED","price":349.99},
    {"name":"Roku Streaming Stick 4K","price":49.99},
    {"name":"Apple TV 4K","price":129.00},
    {"name":"JBL Charge 5 Portable Speaker","price":179.95},
    {"name":"UE Boom 3 Speaker","price":149.99},
    {"name":"Dyson V15 Detect Vacuum","price":699.99},
    {"name":"iRobot Roomba i3+","price":549.99},
    {"name":"Instant Pot Duo 7-in-1","price":89.99},
    {"name":"KitchenAid Artisan Stand Mixer","price":379.99},
    {"name":"Ninja Air Fryer Max XL","price":159.99},
    {"name":"Breville Barista Express Espresso Machine","price":699.95},
    {"name":"Philips Sonicare Electric Toothbrush","price":89.99},
    {"name":"Oral-B iO Series 9","price":299.99},
    {"name":"TCL 50\" 4K Smart TV","price":329.99},
    {"name":"Samsung 65\" QLED TV","price":1199.99},
    {"name":"LG 55\" OLED TV","price":1399.99},
    {"name":"Sony 75\" LED Smart TV","price":1799.99},
    {"name":"Sealy Queen Mattress","price":799.00},
    {"name":"Tempur-Pedic ProAdapt","price":2499.00},
    {"name":"Herman Miller Aeron Chair","price":1199.00},
    {"name":"Ikea Markus Office Chair","price":199.00},
    {"name":"AmazonBasics Monitor Stand","price":29.99},
    {"name":"BenQ 27\" 144Hz Gaming Monitor","price":329.99},
    {"name":"LG Ultrawide 34\" Monitor","price":499.99},
    {"name":"Anova Precision Cooker Sous Vide","price":199.99},
    {"name":"SodaStream Fizzi Sparkling Water Maker","price":99.99},
    {"name":"Eero Pro 6 Mesh Wi-Fi Router","price":299.99},
    {"name":"Netgear Nighthawk AX12 Router","price":399.99},
    {"name":"Tile Mate (4-pack)","price":59.99},
    {"name":"Philips Hue Lightstrip Plus (2m)","price":79.99},
    {"name":"August Smart Lock Pro","price":229.99},
    {"name":"TP-Link Kasa Smart Plug (4 pack)","price":39.99},
    {"name":"Roku Streambar","price":129.99},
    {"name":"Makita Cordless Drill Kit","price":149.99},
    {"name":"DeWalt 20V Max Drill Combo Kit","price":349.99},
    {"name":"Fisher-Price Baby Gym","price":49.99},
    {"name":"Graco 4Ever DLX Car Seat","price":299.99},
    {"name":"Ugg Classic Short Boots","price":139.99},
    {"name":"Nike Air Zoom Pegasus 38","price":119.99},
    {"name":"Adidas Ultraboost 22","price":179.99},
    {"name":"Ray-Ban Wayfarer Sunglasses","price":154.00},
    {"name":"Fossil Gen 6 Smartwatch","price":299.99},
    {"name":"Tile Pro Tracker (2-pack)","price":69.99},
    {"name":"Victorinox Swiss Army Knife","price":39.95},
    {"name":"Carhartt Rugged Work Jacket","price":129.99},
]

CATEGORIES = [
    "Electronics",
    "Computers & Tablets",
    "Audio",
    "Wearables",
    "Cameras",
    "Smart Home",
    "TV & Video",
    "Home Appliances",
    "Kitchen",
    "Office & Furniture",
    "Tools & Outdoor",
    "Baby & Kids",
    "Apparel",
    "Accessories",
]


async def create_users(session:AsyncSession)->list[User]:
    created:list[User] = []
    for u in USERS:
        existing = (await session.execute(
            select(User).where(User.email == u['email'])
        )).scalar_one_or_none()
        if existing is not None:
            created.append(existing)
            continue
        user = User(
            name=u['name'] ,
            email=u['email'] ,
            password_hash=Security.hash_password(u['password']) ,
            role=u['role'] ,
        )
        session.add(user)
        await session.flush()
        profile = Profile(
            user_id=user.id ,
            bio=f"Hello, I'm {u['name']}",
            avatar_url=None
        )
        session.add(profile)
        await session.flush()
        created.append(user)
    return created

async def create_categories(session:AsyncSession)->list[Category]:
    created:list[Category] = []
    for name in CATEGORIES :
        existing = (await session.execute(
            select(Category).where(Category.name == name)
        )).scalar_one_or_none()
        if existing is not None:
            created.append(existing)
            continue
        cat = Category(name=name)
        session.add(cat)
        await session.flush()
        created.append(cat)
    return created

async def create_products_and_link(session:AsyncSession , categories:list[Category])->list[Product]:
    created:list[Product] = []
    for  i,p in enumerate(PRODUCTS):
        existing = (await session.execute(
            select(Product).where(Product.name == p['name'])
        )).scalar_one_or_none()
        if existing is not None : 
            created.append(existing)
            continue
        prod = Product(name=p["name"], price=p["price"])
        prod.categories.append(categories[0])
        if i % 2 == 0 : 
            prod.categories.append(categories[1])
        else :
            prod.categories.append(categories[2])
        session.add(prod)
        await session.flush()
        created.append(prod)
    return created

async def create_orders(session:AsyncSession  , users:list[User] , products:list[Product])->list[Order]:
    created:list[Order] = []
    for u in users:
        if u.role == 'admin':
            continue
        order = Order(user_id = u.id)
        session.add(order)
        await session.flush()
        prods = random.sample(products ,2)
        for prod in prods:
            oi = OrderItem(order_id=order.id , product_id=prod.id , quantity=1 , unit_price=prod.price)
            session.add(oi)
    return created
 
async def run_seed():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            print(".............................................")
            print("........Creating users + profiles............")
            users = await create_users(session)
            print(f"......Created/loaded {len(users)} users......")
            print(".............................................")
            
            print(".............................................")
            print(".............Creating categories.............")
            categories = await create_categories(session)
            print(f"Created/loaded {len(categories)} categories")
            print(".............................................")
            
            print(".............................................")
            print("..Creating products and linking categories..")
            products = await create_products_and_link(session, categories)
            print(f"...Created/loaded {len(products)} products...")
            print(".............................................")
            
            print(".............................................")
            print("..........Creating orders for users..........")
            await create_orders(session, users, products)
            print("...............Orders created...............")
            print(".............................................")
            
if __name__ == '__main__':
    asyncio.run(run_seed())