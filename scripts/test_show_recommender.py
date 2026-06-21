from skill_executors.show_recommender import execute


result = execute(
    "1977/05/08",
    top_n=10
)

print(result["answer"])
print()

for rec in result["recommendations"]:
    print(rec)