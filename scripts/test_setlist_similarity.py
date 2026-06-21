from skill_executors.setlist_similarity import execute


result = execute(
    "1977/05/08",
    "1977/06/08"
)

print(result["answer"])
print()
print(result)