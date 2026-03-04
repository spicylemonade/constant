"""
Utility to update research rubric item status.

Updates a single item in research_rubric.json and recomputes summary counts.

Usage:
    python update_rubric.py <item_id> <status> [error] [notes]
    python update_rubric.py item_001 completed "" "Done with analysis"
"""
import json
import sys

def update_rubric(item_id, status, error=None, notes=None):
    with open('research_rubric.json', 'r') as f:
        data = json.load(f)
    
    found = False
    for phase in data['phases']:
        for item in phase['items']:
            if item['id'] == item_id:
                item['status'] = status
                if error: item['error'] = error
                if notes: item['notes'] = notes
                found = True
                break
        if found: break
        
    counts = {'completed': 0, 'in_progress': 0, 'failed': 0, 'pending': 0}
    for phase in data['phases']:
        for item in phase['items']:
            counts[item['status']] += 1
            
    data['summary'].update(counts)
    
    with open('research_rubric.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    update_rubric(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3] if len(sys.argv) > 3 else None,
        sys.argv[4] if len(sys.argv) > 4 else None,
    )
