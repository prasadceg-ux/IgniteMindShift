"""Seed schools on first startup if the table is empty."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.school import School
from app.models.district import SchoolDistrict

SCHOOLS_BY_DISTRICT: dict[str, list[str]] = {
    "Aldine ISD": ["Aldine High School", "Carver High School", "MacArthur High School", "Nimitz High School", "Eisenhower High School"],
    "Allen ISD": ["Allen High School", "Lowery Freshman Center"],
    "Alvin ISD": ["Alvin High School", "Shadow Creek High School", "Manvel High School"],
    "Amarillo ISD": ["Amarillo High School", "Caprock High School", "Palo Duro High School", "Tascosa High School"],
    "Arlington ISD": ["Arlington High School", "Bowie High School", "Lamar High School", "Martin High School", "Sam Houston High School", "Seguin High School"],
    "Austin ISD": ["Anderson High School", "Austin High School", "Bowie High School", "Crockett High School", "Del Valle High School", "Eastside Memorial High School", "LBJ Early College High School", "McCallum High School", "Reagan High School", "Travis High School"],
    "Beaumont ISD": ["Beaumont United High School", "Central Medical Magnet High School", "West Brook High School"],
    "Brownsville ISD": ["Brownsville Early College High School", "Hanna High School", "Lopez High School", "Porter High School", "Rivera High School"],
    "Carrollton-Farmers Branch ISD": ["Creekview High School", "Farmers Branch High School", "Newman Smith High School", "R.L. Turner High School"],
    "Clear Creek ISD": ["Clear Brook High School", "Clear Creek High School", "Clear Falls High School", "Clear Lake High School", "Clear Springs High School"],
    "Conroe ISD": ["Caney Creek High School", "College Park High School", "Conroe High School", "Grand Oaks High School", "Oak Ridge High School", "The Woodlands High School", "Woodlands College Park High School"],
    "Corpus Christi ISD": ["Carroll High School", "Flour Bluff High School", "King High School", "Miller High School", "Veterans Memorial High School", "W.B. Ray High School"],
    "Crowley ISD": ["Crowley High School", "North Crowley High School"],
    "Cypress-Fairbanks ISD": ["Bridgeland High School", "Cypress Creek High School", "Cypress Falls High School", "Cypress Lakes High School", "Cypress Ranch High School", "Cypress Ridge High School", "Cypress Springs High School", "Cypress Woods High School", "Jersey Village High School"],
    "Dallas ISD": ["Bryan Adams High School", "Conrad High School", "Hillcrest High School", "Kimball High School", "Lincoln High School", "Molina High School", "North Dallas High School", "Skyline High School", "South Oak Cliff High School", "Sunset High School", "W.T. White High School", "Woodrow Wilson High School"],
    "Denton ISD": ["Braswell High School", "Denton High School", "Guyer High School", "Ryan High School"],
    "Ector County ISD": ["Ector County High School", "Odessa High School", "Permian High School"],
    "El Paso ISD": ["Austin High School", "Bel Air High School", "Burges High School", "Eastwood High School", "El Paso High School", "Irvin High School", "Jefferson High School", "Riverside High School"],
    "Edinburg CISD": ["Edinburg High School", "Edinburg North High School", "Edinburg Vela High School"],
    "Fort Bend ISD": ["Austin High School", "Bush High School", "Clements High School", "District Alternative Education Program", "Elkins High School", "Hightower High School", "Kempner High School", "Marshall High School", "Ridge Point High School", "Travis High School"],
    "Fort Worth ISD": ["Arlington Heights High School", "Brewer High School", "Castleberry High School", "Eastern Hills High School", "Northside High School", "Paschal High School", "South Hills High School", "Wyatt High School"],
    "Frisco ISD": ["Centennial High School", "Frisco High School", "Heritage High School", "Lebanon Trail High School", "Liberty High School", "Lone Star High School", "Panther Creek High School", "Reedy High School"],
    "Garland ISD": ["Garland High School", "Lakeview Centennial High School", "Naaman Forest High School", "Rowlett High School", "South Garland High School"],
    "Grand Prairie ISD": ["Grand Prairie High School", "South Grand Prairie High School"],
    "Grapevine-Colleyville ISD": ["Colleyville Heritage High School", "Grapevine High School"],
    "Harlingen CISD": ["Harlingen High School", "Harlingen South High School"],
    "Houston ISD": ["Austin High School", "Bellaire High School", "Carnegie Vanguard High School", "Challenge Early College High School", "Davis High School", "DeBakey High School for Health Professions", "Furr High School", "Kashmere High School", "Lamar High School", "Lee High School", "Madison High School", "Milby High School", "North Houston Early College High School", "Northside High School", "Scarborough High School", "Sterling High School", "Waltrip High School", "Washington High School", "Westbury High School", "Westside High School", "Wheatley High School", "Worthing High School", "Yates High School"],
    "Humble ISD": ["Atascocita High School", "Humble High School", "Kingwood High School", "Summer Creek High School"],
    "Irving ISD": ["Irving High School", "Nimitz High School", "MacArthur High School"],
    "Judson ISD": ["Judson High School", "Wagner High School"],
    "Katy ISD": ["Cinco Ranch High School", "Jordan High School", "Katy High School", "Morton Ranch High School", "Seven Lakes High School", "Taylor High School", "Tompkins High School"],
    "Killeen ISD": ["Ellison High School", "Harker Heights High School", "Killeen High School", "Shoemaker High School"],
    "Klein ISD": ["Klein Collins High School", "Klein Forest High School", "Klein High School", "Klein Oak High School"],
    "Lamar CISD": ["George Ranch High School", "Lamar Consolidated High School", "Randle High School", "Terry High School"],
    "Lewisville ISD": ["The Colony High School", "Flower Mound High School", "Hebron High School", "Lewisville High School", "Marcus High School"],
    "Longview ISD": ["Longview High School", "Pine Tree High School"],
    "Lubbock ISD": ["Lubbock High School", "Monterey High School", "Coronado High School"],
    "Mansfield ISD": ["Mansfield High School", "Mansfield Lake Ridge High School", "Mansfield Summit High School", "Timberview High School"],
    "McAllen ISD": ["McAllen High School", "McAllen Memorial High School"],
    "McKinney ISD": ["McKinney Boyd High School", "McKinney High School", "McKinney North High School"],
    "Mesquite ISD": ["Horn High School", "John Horn High School", "Mesquite High School", "North Mesquite High School", "Poteet High School", "West Mesquite High School"],
    "Midland ISD": ["Lee High School", "Midland High School"],
    "New Braunfels ISD": ["New Braunfels High School", "Canyon High School"],
    "North East ISD": ["Churchill High School", "Johnson High School", "Lee High School", "MacArthur High School", "Madison High School", "Reagan High School"],
    "Northside ISD": ["Clark High School", "Holmes High School", "Brandeis High School", "Harlan High School", "O'Connor High School", "Sotomayor High School", "Stevens High School", "Taft High School"],
    "Pasadena ISD": ["Dobie High School", "Memorial High School", "Pasadena High School", "Sam Rayburn High School", "South Houston High School"],
    "Pflugerville ISD": ["Hendrickson High School", "Pflugerville High School", "Weiss High School"],
    "Plano ISD": ["Plano East Senior High School", "Plano Senior High School", "Plano West Senior High School"],
    "Richardson ISD": ["J.J. Pearce High School", "Lake Highlands High School", "Richardson High School"],
    "Round Rock ISD": ["Cedar Ridge High School", "McNeil High School", "Round Rock High School", "Stony Point High School", "Westwood High School"],
    "San Antonio ISD": ["Brackenridge High School", "Edison High School", "Fox Tech High School", "Jefferson High School", "Lanier High School", "Burbank High School", "Memorial High School"],
    "Socorro ISD": ["Americas High School", "Eastlake High School", "El Dorado High School", "Socorro High School"],
    "Spring Branch ISD": ["Northbrook High School", "Memorial High School", "Spring Branch High School", "Stratford High School"],
    "Spring ISD": ["Dekaney High School", "Spring High School", "Westfield High School"],
    "Tyler ISD": ["John Tyler High School", "Robert E. Lee High School"],
    "Waco ISD": ["Waco High School", "University High School"],
    "Wichita Falls ISD": ["Hirschi High School", "Rider High School", "Wichita Falls High School"],
    "Ysleta ISD": ["Bel Air High School", "Eastwood High School", "Parkland High School", "Riverside High School", "Ysleta High School"],
}


async def seed_schools(db: AsyncSession) -> None:
    result = await db.execute(select(School).limit(1))
    if result.scalar_one_or_none():
        return  # Already seeded

    # Load districts by name
    districts_result = await db.execute(select(SchoolDistrict))
    district_map = {d.name: d.id for d in districts_result.scalars().all()}

    count = 0
    for district_name, school_names in SCHOOLS_BY_DISTRICT.items():
        district_id = district_map.get(district_name)
        if not district_id:
            continue
        for school_name in school_names:
            db.add(School(district_id=district_id, name=school_name))
            count += 1

    await db.flush()
    print(f"✓ Seeded {count} schools")
