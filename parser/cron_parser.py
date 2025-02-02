
import sys

def parse_field(field,min_val, max_val):
    """Parse a invidual cron field."""
    values = []
    
    for part in field.split(','):
        if part == '*':
            values.extend(range(min_val, max_val + 1))
            continue

        # Handle step values (e.g., */15 or 1-5/2)
        if '/' in part:
            base, step = part.split('/')
            step = int(step)
            if base == '*':
                base = f"{min_val}-{max_val}"
        else:
            base, step = part, 1
            
        # Handle ranges (e.g., 1-5)
        if '-' in base:
            start, end = map(int, base.split('-'))
        else:
            start = end = int(base)
            
        # Validate range
        if not (min_val <= start <= end <= max_val):
            raise ValueError(f"Invalid range {start}-{end} for {min_val}-{max_val}")
            
        values.extend(range(start, end + 1, step))

    return values

def parse_cron(cron_str):
    """Parse full cron string."""

    FIELDS = [
        ('minute', 0, 59),
        ('hour', 0, 23),
        ('day of month', 1, 31),
        ('month', 1, 12),
        ('day of week', 0, 6),
    ]

    parts = cron_str.split()
    if len(parts) < 6:
        raise ValueError("Invalid cron format - needs 5 time fields + command")
    
    result = {}
    for i, (name, min_val, max_val) in enumerate(FIELDS):
        result[name] = parse_field(parts[i], min_val, max_val)
    
    result['command'] = ' '.join(parts[5:])
    return result

def format_output(result):
    """Print output in seperate line."""
    output = []
    for key, value in result.items():
        sval = [str(a) for a in value ]
        if key != 'command':
            output.append(f"{key.ljust(14)}{" ".join(sval)}")
    output.append(f"{'command'.ljust(14)}{result['command']}")
    return '\n'.join(output)
    
def main():
    """CLI entry point."""
    if len(sys.argv) != 2:
        print("Usage: cron_parser <cron_string>")
        sys.exit(1)
    
    try:
        parsed = parse_cron(sys.argv[1])
        print(format_output(parsed))
       
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()