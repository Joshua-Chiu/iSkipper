if [[ -z "$VIRTUAL_ENV" ]]; then
    source venv/bin/activate
else
    echo "venv is set"
fi

python iSkipper.py headless
