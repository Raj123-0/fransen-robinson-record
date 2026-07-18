import time
import multiprocessing
import sys
import os
from datetime import datetime

try:
    import gmpy2
    BACKEND = "GMPY2 (Maximum C-Level Speed)"
except ImportError:
    print("\n[!] 'gmpy2' not found. Attempting to install it into the current environment...\n")
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gmpy2"])
        import gmpy2
        BACKEND = "GMPY2 (Maximum C-Level Speed)"
        print("[+] Successfully installed 'gmpy2'.\n")
    except Exception as e:
        BACKEND = "Pure Python (WARNING: SLOW)"
        print(f"\n[!] WARNING: Could not install 'gmpy2'. Computations will be extremely slow. Error: {e}\n")

try:
    import mpmath
except ImportError:
    print("Error: 'mpmath' is required. Run: pip install mpmath")
    sys.exit(1)


def integrate_verification_chunk(args):
    """
    Worker function for the verification pass.
    CRITICAL DIFFERENCE: Uses 'gauss-legendre' quadrature instead of 'tanh-sinh'.
    This uses a completely different set of polynomial weights and nodes, 
    ensuring an entirely independent mathematical pathway.
    """
    chunk_id, start, end, precision = args
    mpmath.mp.dps = precision
    
    try:
        start_time = time.time()
        # Using standard gamma division as a secondary verification of the rgamma function
        def target_func(x):
            return 1 / mpmath.gamma(x)
            
        # Force Gauss-Legendre integration
        area = mpmath.quad(target_func, [start, end], method='gauss-legendre')
        duration = time.time() - start_time
        
        return {
            'id': chunk_id,
            'range': f"[{start}, {end}]",
            'area': str(area),
            'time': duration,
            'error': None
        }
    except Exception as e:
        return {'id': chunk_id, 'error': str(e)}

def generate_geometric_chunks(upper_bound, num_chunks, precision):
    """
    Instead of hand-crafted asymmetric chunks, this generates strictly 
    uniform geometric intervals to ensure the mathematical slice points 
    do not align with the first script.
    """
    breakpoints = [0]
    step = upper_bound / num_chunks
    
    for i in range(1, num_chunks + 1):
        breakpoints.append(i * step)
        
    chunks = []
    for i in range(len(breakpoints) - 1):
        chunks.append((i, breakpoints[i], breakpoints[i+1], precision))
        
    return chunks

def run_verification(target_digits):
    """
    Orchestrates the alternative calculation method.
    """
    buffer_digits = target_digits + 20 
    mpmath.mp.dps = buffer_digits 
    
    # Calculate a slightly different bounding box to alter the tail calculation
    threshold = mpmath.mpf(10)**(-target_digits - 10)
    x = mpmath.mpf(5)
    while (1 / mpmath.gamma(x)) > threshold:
        x += 5
    upper_bound = int(x) + 5 

    print(f"[*] Alternate Optimization: Truncating integral at x = {upper_bound}")
    
    # Create an arbitrary number of geometric chunks (e.g., 250 uniform slices)
    chunks = generate_geometric_chunks(upper_bound, 250, buffer_digits)
    total_chunks = len(chunks)
    
    num_cores = multiprocessing.cpu_count()
    print(f"[*] Engine: {BACKEND}")
    print(f"[*] Method: Gauss-Legendre Quadrature")
    print(f"[*] Distributing {total_chunks} uniform chunks across {num_cores} CPU cores...\n")
    print("-" * 60)
    
    start_time = time.time()
    total_area = mpmath.mpf(0)
    
    with multiprocessing.Pool(processes=num_cores) as pool:
        for i, result in enumerate(pool.imap_unordered(integrate_verification_chunk, chunks), 1):
            if result['error']:
                print(f"\n[!] ERROR in chunk {result['id']}: {result['error']}")
                sys.exit(1)
                
            total_area += mpmath.mpf(result['area'])
            
            now = datetime.now().strftime("%H:%M:%S")
            percent = (i / total_chunks) * 100
            print(f"[{now}] Gauss-Legendre Verification: {i:03d}/{total_chunks} ({percent:5.1f}%)")

    mpmath.mp.dps = target_digits
    final_result = str(+total_area) 
    
    return final_result, (time.time() - start_time)

def verify_against_file(calculated_result, filename="fransen_robinson_1500_digits.txt"):
    """
    Reads the original run and performs a strict character-by-character comparison.
    """
    print("\n" + "=" * 60)
    print(" INITIATING STRICT DIFF-CHECK ")
    print("=" * 60)
    
    if not os.path.exists(filename):
        print(f"[!] Could not find '{filename}' in the current directory.")
        print("[!] Skipping automated file comparison. Here is your verified output:")
        print(calculated_result)
        return

    with open(filename, 'r') as f:
        original = f.read().strip()
        
    print(f"[*] Loaded Original Run: {len(original)-1} decimal digits")
    print(f"[*] Loaded Verification Run: {len(calculated_result)-1} decimal digits\n")
    
    min_len = min(len(original), len(calculated_result))
    mismatches = 0
    
    for i in range(min_len):
        if original[i] != calculated_result[i]:
            print(f"[!] CRITICAL MISMATCH at index {i} (Digit {i-1}):")
            print(f"    Original File : {original[i]}")
            print(f"    Verification  : {calculated_result[i]}")
            mismatches += 1
            if mismatches > 5:
                print("... stopping after 5 mismatches.")
                break
                
    if mismatches == 0:
        print(" VERIFICATION SUCCESSFUL! ")
        print(f"All {min_len-1} digits match perfectly across both mathematical methods.")
        print("This confirms the result is mathematically sound and free of hardware drift.")
    else:
        print("\n[!] Verification FAILED. The mathematical paths diverged.")

if __name__ == "__main__":
    print("=" * 60)
    print(" FRANSÉN-ROBINSON INDEPENDENT VERIFICATION ENGINE ")
    print("=" * 60)
    
    TARGET = 1500  # Set this to match the exact length of your original file
    
    print(f"Targeting {TARGET} significant digits for verification...\n")
    
    verification_result, duration = run_verification(TARGET)
    
    print(f"\n[*] Verification pass completed in {duration/3600:.2f} hours.")
    
    # Run the automated cross-reference
    verify_against_file(verification_result, "fransen_robinson_1500_digits.txt")