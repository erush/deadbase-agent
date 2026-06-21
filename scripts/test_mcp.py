from mcp_server.tools import (
    find_show,
    find_song,
    find_venue
)


print("\nSHOW\n")
print(
    find_show("1977/05/08")
)

print("\nSONG\n")
print(
    find_song("Dark Star")[:5]
)

print("\nVENUE\n")
print(
    find_venue("Winterland")[:5]
)