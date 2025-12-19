import asyncio
from mosstool.type import Persons
from mosstool.trip.route import RoutingClient, pre_route

IN_FILE = "data/person.pb"
OUT_FILE = "data/person_routed.pb"
ROUTING_URL = "http://localhost:52101"

async def main():
    pb = Persons()
    pb.ParseFromString(open(IN_FILE, "rb").read())

    client = RoutingClient(ROUTING_URL)

    out_persons = []
    for p in pb.persons:
        p2 = await pre_route(client, p)
        # 保守过滤：避免生成失败的 trip
        if p2.schedules and p2.schedules[0].trips:
            out_persons.append(p2)

    out = Persons(persons=out_persons)
    open(OUT_FILE, "wb").write(out.SerializeToString())
    print(f"routed persons: {len(out_persons)} / {len(pb.persons)} -> {OUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
