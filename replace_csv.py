import pandas as pd

# Load files
npc_df = pd.read_csv("NPC_list.csv", encoding="ISO-8859-1")
consumer_df = pd.read_csv("1012_Corporate_Roaming_Zone.csv", encoding="ISO-8859-1")

# Clean and normalize all columns
def clean(series):
    return (
        series.astype(str)
        .str.replace(r"[\s\u200b\r\n]+", "", regex=True)
        .str.upper()
    )

npc_df["NPC_List"] = clean(npc_df["NPC_List"])
npc_df["PCSList/BGW"] = clean(npc_df["PCSList/BGW"])
npc_df["TADIG Code"] = npc_df["TADIG Code"].astype(str).str.strip()  # Keep TADIG as-is
consumer_df["NPC_LIST::value"] = clean(consumer_df["NPC_LIST::value"])

# Combine NPC_List and PCSList/BGW into one dictionary
combined_df = pd.concat([
    npc_df[["NPC_List", "TADIG Code"]].rename(columns={"NPC_List": "key"}),
    npc_df[["PCSList/BGW", "TADIG Code"]].rename(columns={"PCSList/BGW": "key"})
], ignore_index=True)

# Remove duplicates and build mapping
combined_df = combined_df.dropna().drop_duplicates(subset="key")
mapping = dict(zip(combined_df["key"], combined_df["TADIG Code"]))

# Apply mapping
consumer_df["TADIG_Match"] = consumer_df["NPC_LIST::value"].map(mapping)

# Split matched and unmatched
matched_df = consumer_df[consumer_df["TADIG_Match"].notna()].copy()
unmatched_df = consumer_df[consumer_df["TADIG_Match"].isna()].copy()

# Replace NPC_LIST::value with TADIG match
matched_df["NPC_LIST::value"] = matched_df["TADIG_Match"]
matched_df = matched_df.drop(columns=["TADIG_Match"])
unmatched_df = unmatched_df.drop(columns=["TADIG_Match"])

# Save results
matched_df.to_csv("1012_Replaced.csv", index=False, encoding="utf-8")
unmatched_df.to_csv("1012_Unmatched.csv", index=False, encoding="utf-8")

print("✅ Case-insensitive replacement complete!")
print("✔ created: 1012_Replaced.csv")
print("❌ Unmatched: 1012_Unmatched.csv")

