two-level hierarchy: local area, backbone.
link-state advertisements only in area 
each nodes has detailed area topology; only know direction (shortest path) to nets in other areas.
area border routers: “summarize” distances  to nets in own area, advertise to other Area Border routers.
backbone routers: run OSPF routing limited to backbone.
boundary routers: connect to other AS’es.

