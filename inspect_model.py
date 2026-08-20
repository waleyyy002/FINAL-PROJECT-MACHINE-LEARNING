import joblib
import sys

path = "customer_churn_prediction.pkl"

try:
    m = joblib.load(path)
except Exception as e:
    print("failed to load:", e)
    sys.exit(1)

print("type:", type(m))

if isinstance(m, dict):
    print("dict keys:")
    for k in m.keys():
        print(" -", k)
    print("\nDetails for each key:\n")
    for k, v in m.items():
        print(f"== {k} ({type(v)}) ==")
        # try common sklearn attributes
        for attr in ("feature_names_in_", "n_features_in_"):
            if hasattr(v, attr):
                print(f" - {attr}:", getattr(v, attr))
        # if it's a dict (like label_encoders), show keys
        if isinstance(v, dict):
            print(" - dict keys:")
            for subk in v.keys():
                print("    -", subk)
        # if it's an sklearn estimator, show classes_ if present
        if hasattr(v, "classes_"):
            try:
                print(" - classes_ (sample):", getattr(v, "classes_")[:10])
            except Exception:
                pass
        # show n_features_in_ if present
        if hasattr(v, "n_features_in_"):
            try:
                print(" - n_features_in_:", getattr(v, "n_features_in_"))
            except Exception:
                pass
        print()
else:
    print("repr:", repr(m)[:500])
    print("dir (filtered):")
    for a in [x for x in dir(m) if not x.startswith("__")][:200]:
        print(" -", a)

sys.exit(0)
