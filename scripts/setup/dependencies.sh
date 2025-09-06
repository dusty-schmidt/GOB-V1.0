#!/bin/bash
# File: scripts/setup/dependencies.sh
# Location: GOBV1 project setup dependencies management
# Role: Optimized dependency installation with mamba batch processing and intelligent package splitting

# Source utilities
source "$(dirname "${BASH_SOURCE[0]}")/utils.sh"

install_dependencies() {
    print_status "step" "Installing dependencies from requirements.txt..."
    
    # Check if requirements.txt exists
    if [ ! -f "$PROJECT_DIR/requirements.txt" ]; then
        print_status "error" "requirements.txt not found in project root"
        print_status "info" "Please ensure requirements.txt exists with version-pinned dependencies"
        exit 1
    fi
    
    # Prepare logging
    ensure_dir "$PROJECT_DIR/logs"
    local log_file="$PROJECT_DIR/logs/dependencies.log"
    : > "$log_file"
    echo "$(date): Starting optimized dependency installation" >> "$log_file"

    # Parse requirements.txt into conda-forge vs pip-only packages
    declare -a CONDAPKGS
    declare -a PIPONLY
    declare -a FAILED
    local pip_failed=0

    print_status "info" "Analyzing packages and separating conda-forge from pip-only..."
    
    while IFS= read -r line; do
        # Skip empties and comments
        [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
        
        clean=$(echo "$line" | xargs)
        [[ -z "$clean" ]] && continue
        
        # Extract base package name (remove version specifiers and extras)
        base=$(echo "$clean" | sed 's/\[.*\]//')               # strip extras like [async]
        name=$(echo "$base" | sed 's/[<>=!~].*$//')            # get package name only
        
        # Categorize packages - conda-forge available packages go to mamba
        case "$name" in
            flask|python-dotenv|pytz|markdown|paramiko|psutil|gitpython|tiktoken|nest-asyncio|soundfile|pypdf|webcolors|markdownify|pathspec|faiss-cpu|sentence-transformers|pymupdf|lxml|numpy|pandas|matplotlib|scipy|pillow|beautifulsoup4|nltk|opencv)
                # Convert == to = for conda format
                conda_spec=$(echo "$base" | sed 's/==/=/')
                CONDAPKGS+=("$conda_spec")
                echo "  conda-forge: $conda_spec" >> "$log_file"
                ;;
            *)
                PIPONLY+=("$clean")
                echo "  pip-only: $clean" >> "$log_file"
                ;;
        esac
    done < "$PROJECT_DIR/requirements.txt"

    echo "Categorized ${#CONDAPKGS[@]} conda-forge packages and ${#PIPONLY[@]} pip-only packages" >> "$log_file"
    print_status "info" "Found ${#CONDAPKGS[@]} conda-forge packages, ${#PIPONLY[@]} pip-only packages"

    # Phase 1: Install conda-forge packages with mamba (fast batch install)
    if [ ${#CONDAPKGS[@]} -gt 0 ]; then
        print_status "info" "Installing conda-forge packages with ${CONDA_CMD:-mamba}..."
        show_working "Installing conda packages with ${CONDA_CMD:-mamba}..." & sp=$!
        
        echo "$(date): Installing conda packages: ${CONDAPKGS[*]}" >> "$log_file"
        if ${CONDA_CMD:-mamba} install -n "$CONDA_ENV" -c conda-forge -y "${CONDAPKGS[@]}" >> "$log_file" 2>&1; then
            kill $sp 2>/dev/null; wait $sp 2>/dev/null
            print_status "success" "Conda-forge packages installed successfully"
        else
            kill $sp 2>/dev/null; wait $sp 2>/dev/null
            print_status "warning" "Some conda packages may have failed, continuing with pip..."
            echo "$(date): Conda install had issues, check log above" >> "$log_file"
        fi
    else
        print_status "info" "No conda-forge packages to install"
    fi

    # Phase 2: Upgrade pip (retain cache for speed)
    print_status "info" "Upgrading pip..."
    python -m pip install --upgrade pip >> "$log_file" 2>&1 || true

    # Phase 3: Install remaining packages with pip (single batch)
    if [ ${#PIPONLY[@]} -gt 0 ]; then
        print_status "info" "Installing remaining Python packages with pip..."
        show_working "Installing pip packages (batch mode)..." & sp=$!
        
        echo "$(date): Installing pip packages: ${PIPONLY[*]}" >> "$log_file"
        if pip install "${PIPONLY[@]}" >> "$log_file" 2>&1; then
            kill $sp 2>/dev/null; wait $sp 2>/dev/null
            print_status "success" "Pip packages installed successfully"
        else
            kill $sp 2>/dev/null; wait $sp 2>/dev/null
            pip_failed=1
            print_status "warning" "Some pip packages failed"
            echo "$(date): Pip install had failures" >> "$log_file"
        fi
    else
        print_status "info" "No pip-only packages to install"
    fi

    # Phase 4: Fallback - install entire requirements.txt if pip-only failed
    if [ $pip_failed -eq 1 ]; then
        print_status "info" "Attempting fallback: installing full requirements.txt..."
        show_working "Fallback pip install..." & sp=$!
        
        echo "$(date): Fallback: installing full requirements.txt" >> "$log_file"
        if pip install -r "$PROJECT_DIR/requirements.txt" >> "$log_file" 2>&1; then
            kill $sp 2>/dev/null; wait $sp 2>/dev/null
            print_status "success" "Fallback installation successful"
            pip_failed=0
        else
            kill $sp 2>/dev/null; wait $sp 2>/dev/null
            print_status "warning" "Fallback installation also had issues"
        fi
    fi

    # Phase 5: Optional uv acceleration (if available)
    if command -v uv >/dev/null 2>&1 && [ $pip_failed -eq 1 ]; then
        print_status "info" "Attempting uv-powered installation..."
        show_working "Installing with uv (ultra-fast pip replacement)..." & sp=$!
        
        echo "$(date): Using uv for final attempt" >> "$log_file"
        if uv pip install -r "$PROJECT_DIR/requirements.txt" >> "$log_file" 2>&1; then
            kill $sp 2>/dev/null; wait $sp 2>/dev/null
            print_status "success" "uv installation successful"
            pip_failed=0
        else
            kill $sp 2>/dev/null; wait $sp 2>/dev/null
            print_status "warning" "uv installation also failed"
        fi
    fi

    # Final summary
    echo "$(date): Installation process completed" >> "$log_file"
    if [ $pip_failed -eq 0 ]; then
        print_status "success" "All dependencies installed successfully using optimized batch method"
        print_status "info" "Installation method: mamba (${#CONDAPKGS[@]} pkgs) + pip (${#PIPONLY[@]} pkgs)"
    else
        print_status "warning" "Some packages may have failed - check functionality"
        print_status "info" "Detailed logs available at: $log_file"
        echo "$(date): Final status: some failures occurred" >> "$log_file"
    fi
}
