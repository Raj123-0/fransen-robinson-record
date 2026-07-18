import time
import multiprocessing
import sys
import math

try:
    import mpmath
except ImportError:
    print("Error: 'mpmath' required. Run: pip install mpmath")
    sys.exit(1)

try:
    import gmpy2
except ImportError:
    pass

def integrate_chunk(args):
    chunk_id, start, end, precision = args
    mpmath.mp.dps = precision
    try:
        t0 = time.time()
        # Use Plouffe's integral formula for 1/Gamma(x) which converges much faster: e^-x / (pi^2 + ln^2(x))
        area = mpmath.quad(lambda x: mpmath.exp(-x) / (mpmath.pi**2 + mpmath.log(x)**2), [start, end], method='tanh-sinh')
        return {'id': chunk_id, 'range': f"[{start}, {end}]", 'area': str(area), 'time': time.time() - t0, 'error': None}
    except Exception as e:
        return {'id': chunk_id, 'error': str(e)}

def calculate_finite_boundary(target_digits):
    # e^-x < 10^-target_digits => x > target_digits * ln(10)
    return int(target_digits * math.log(10)) + 5

def generate_chunks(upper_bound, precision):
    # Logarithmic-like chunking for better distribution, function decays rapidly initially
    breakpoints = [0, 1, 5, 10]
    curr = 10
    step = 50
    while curr < upper_bound:
        breakpoints.append(curr)
        curr += step
        step = min(step * 2, 500)  # Increase step size as curve flattens out
    if breakpoints[-1] != upper_bound:
        if upper_bound > breakpoints[-1]:
            breakpoints.append(upper_bound)
        else:
            breakpoints[-1] = upper_bound
    breakpoints = sorted(list(set(breakpoints)))
    return [(i, breakpoints[i], breakpoints[i+1], precision) for i in range(len(breakpoints)-1)]

def calculate_fransen_robinson(target_digits):
    buffer_digits = target_digits + 5 
    mpmath.mp.dps = buffer_digits 
    
    upper_bound = calculate_finite_boundary(buffer_digits)
    chunks = generate_chunks(upper_bound, buffer_digits)
    total_chunks, num_cores = len(chunks), multiprocessing.cpu_count()
    
    print(f"Target: {target_digits} digits | Cores: {num_cores} | Upper Bound: {upper_bound} | Chunks: {total_chunks}\n")
    
    start_time = time.time()
    total_area = mpmath.mpf(0)
    
    with multiprocessing.Pool(processes=num_cores) as pool:
        for i, result in enumerate(pool.imap_unordered(integrate_chunk, chunks), 1):
            if result['error']:
                print(f"\nError in chunk {result['id']}: {result['error']}")
                sys.exit(1)
                
            total_area += mpmath.mpf(result['area'])
            
            elapsed = time.time() - start_time
            percent = i / total_chunks
            eta = (elapsed / i) * (total_chunks - i)
            bar = '=' * int(30 * percent) + '-' * (30 - int(30 * percent))
            
            sys.stdout.write(f"\r[{bar}] {percent*100:5.1f}% | ETA: {eta:.1f}s | Chunk {result['range']} ({result['time']:.2f}s)   ")
            sys.stdout.flush()
            
    print()
    mpmath.mp.dps = target_digits
    # Add 'e' as per Plouffe's formula F = e + int(e^-x / (pi^2 + ln^2(x))) dx
    total_area += mpmath.e
    return str(+total_area), (time.time() - start_time)

if __name__ == "__main__":
    TARGET = 1500
    result, duration = calculate_fransen_robinson(TARGET)
    
    filename = f"fransen_robinson_{TARGET}_digits.txt"
    with open(filename, "w") as f:
        f.write(result)
        
    print(f"\nCompleted in {duration:.2f}s")
    print(f"Output saved to: {filename}")
    print(f"Preview: {result[:60]}...")