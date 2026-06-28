from pathlib import Path
import duckdb
import pandas as pd
import numpy as np

DB_PATH = (
    Path(__file__)
    .parent.parent
    / "data"
    / "duckdb"
    / "deadbase.duckdb"
)

def main():
    con = duckdb.connect(str(DB_PATH))
    
    # Read all rows from show_profile
    show_profile_df = con.execute("SELECT * FROM show_profile").fetchdf()
    
    # Read performances into a DataFrame
    performances_df = con.execute("""
        SELECT show_uuid, set_number, song_position, song_uuid, segued
        FROM performances
    """).fetchdf()
    
    # Prepare list to collect DNA rows
    dna_rows = []
    
    # Group performances by show_uuid for quick access
    performances_grouped = performances_df.groupby('show_uuid')
    
    for _, show_row in show_profile_df.iterrows():
        show_uuid = show_row['show_uuid']
        
        if show_uuid in performances_grouped.groups:
            # Get performances for this show
            show_performances = performances_grouped.get_group(show_uuid)
            
            # Compute DNA metrics
            show_length = len(show_performances)
            song_count = show_performances['song_uuid'].count()
            unique_song_count = show_performances['song_uuid'].nunique()
            set_count = show_performances['set_number'].nunique()
            first_set_count = (show_performances['set_number'] == 1).sum()
            second_set_count = (show_performances['set_number'] == 2).sum()
            third_set_plus_count = (show_performances['set_number'] >= 3).sum()
            segued_count = show_performances['segued'].sum()
            segue_ratio = segued_count / show_length if show_length > 0 else None
            
            has_performance_data = True
            dna_complete = True
        else:
            # Metadata-only row
            show_length = 0
            song_count = 0
            unique_song_count = 0
            set_count = 0
            first_set_count = 0
            second_set_count = 0
            third_set_plus_count = 0
            segued_count = 0
            segue_ratio = None
            
            has_performance_data = False
            dna_complete = False
        
        dna_row = {
            'show_uuid': show_uuid,
            'show_date': show_row['show_date'],
            'year': show_row['year'],
            'era': show_row['era'],
            'venue': show_row['venue'],
            'city': show_row['city'],
            'state': show_row['state'],
            'country': show_row['country'],
            'has_performance_data': has_performance_data,
            'dna_complete': dna_complete,
            'show_length': show_length,
            'song_count': song_count,
            'unique_song_count': unique_song_count,
            'set_count': set_count,
            'first_set_count': first_set_count,
            'second_set_count': second_set_count,
            'third_set_plus_count': third_set_plus_count,
            'segued_count': segued_count,
            'segue_ratio': segue_ratio
        }
        dna_rows.append(dna_row)
    
    dna_df = pd.DataFrame(dna_rows)
    
    # Write resulting DataFrame back to show_dna table
    con.register('dna_df', dna_df)
    con.execute('CREATE OR REPLACE TABLE show_dna AS SELECT * FROM dna_df')
    
    total_rows = len(dna_df)
    complete_dna_rows = dna_df['dna_complete'].sum()
    metadata_only_rows = total_rows - complete_dna_rows
    
    print(f"total_rows={total_rows}")
    print(f"complete_dna_rows={complete_dna_rows}")
    print(f"metadata_only_rows={metadata_only_rows}")
    
    con.close()

if __name__ == '__main__':
    main()
