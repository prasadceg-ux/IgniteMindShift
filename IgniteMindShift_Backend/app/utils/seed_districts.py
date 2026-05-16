"""Seed school districts on first startup if the table is empty."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.district import SchoolDistrict

DISTRICTS = [
    ("Aldine ISD", "TX"),
    ("Allen ISD", "TX"),
    ("Alvin ISD", "TX"),
    ("Amarillo ISD", "TX"),
    ("Arlington ISD", "TX"),
    ("Austin ISD", "TX"),
    ("Beaumont ISD", "TX"),
    ("Brownsville ISD", "TX"),
    ("Carrollton-Farmers Branch ISD", "TX"),
    ("Clear Creek ISD", "TX"),
    ("Conroe ISD", "TX"),
    ("Corpus Christi ISD", "TX"),
    ("Crowley ISD", "TX"),
    ("Cypress-Fairbanks ISD", "TX"),
    ("Dallas ISD", "TX"),
    ("Denton ISD", "TX"),
    ("Ector County ISD", "TX"),
    ("El Paso ISD", "TX"),
    ("Edinburg CISD", "TX"),
    ("Fort Bend ISD", "TX"),
    ("Fort Worth ISD", "TX"),
    ("Frisco ISD", "TX"),
    ("Galveston ISD", "TX"),
    ("Garland ISD", "TX"),
    ("Grand Prairie ISD", "TX"),
    ("Grapevine-Colleyville ISD", "TX"),
    ("Harlingen CISD", "TX"),
    ("Houston ISD", "TX"),
    ("Humble ISD", "TX"),
    ("Irving ISD", "TX"),
    ("Judson ISD", "TX"),
    ("Katy ISD", "TX"),
    ("Killeen ISD", "TX"),
    ("Klein ISD", "TX"),
    ("Lamar CISD", "TX"),
    ("Lewisville ISD", "TX"),
    ("Longview ISD", "TX"),
    ("Lubbock ISD", "TX"),
    ("Mansfield ISD", "TX"),
    ("McAllen ISD", "TX"),
    ("McKinney ISD", "TX"),
    ("Mesquite ISD", "TX"),
    ("Midland ISD", "TX"),
    ("New Braunfels ISD", "TX"),
    ("North East ISD", "TX"),
    ("Northside ISD", "TX"),
    ("Pasadena ISD", "TX"),
    ("Pflugerville ISD", "TX"),
    ("Plano ISD", "TX"),
    ("Richardson ISD", "TX"),
    ("Round Rock ISD", "TX"),
    ("San Antonio ISD", "TX"),
    ("Socorro ISD", "TX"),
    ("Spring Branch ISD", "TX"),
    ("Spring ISD", "TX"),
    ("Tyler ISD", "TX"),
    ("Waco ISD", "TX"),
    ("Wichita Falls ISD", "TX"),
    ("Ysleta ISD", "TX"),
]


async def seed_districts(db: AsyncSession) -> None:
    result = await db.execute(select(SchoolDistrict).limit(1))
    if result.scalar_one_or_none():
        return  # Already seeded

    for name, state in DISTRICTS:
        db.add(SchoolDistrict(name=name, state=state))

    await db.flush()
    print(f"✓ Seeded {len(DISTRICTS)} school districts")
