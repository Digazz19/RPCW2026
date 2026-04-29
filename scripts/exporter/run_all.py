import subprocess
import sys
import time

# List of all exporter scripts in a logical order
EXPORTERS = [
    "enchantments_exporter.py",
    "effects_exporter.py",
    "item_exporter.py",
    "foods_exporter.py",
    "blocks_exporter.py",
    "entities_exporter.py",
    "biomes_exporter.py",
    "recipies_exporter.py"
]

def run_all():
    print("="*50)
    print("⛏️  Starting Minecraft Ontology Export Process")
    print("="*50)
    
    start_time = time.time()
    successful_runs = 0

    for script in EXPORTERS:
        print(f"\n▶ Executing: {script} ...")
        try:
            # sys.executable ensures it uses the same Python environment (e.g., your venv)
            subprocess.run([sys.executable, script], check=True)
            successful_runs += 1
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error: '{script}' failed with exit code {e.returncode}.")
            print("🛑 Halting execution. Please fix the error above before continuing.")
            break
        except FileNotFoundError:
            print(f"\n❌ Error: Could not find '{script}'.")
            print("Make sure you are running this script from inside the 'scripts/' directory.")
            break

    elapsed_time = time.time() - start_time
    
    print("\n" + "="*50)
    if successful_runs == len(EXPORTERS):
        print(f"✅ All {successful_runs} exporters finished successfully in {elapsed_time:.2f} seconds!")
        print("You can now import the generated .ttl files into GraphDB.")
    else:
        print(f"⚠️ Process aborted. {successful_runs}/{len(EXPORTERS)} scripts completed.")
    print("="*50)

if __name__ == "__main__":
    run_all()