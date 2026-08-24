import joblib

model = joblib.load("anomaly_model.joblib")

print("Type:", type(model))
print()
print(model)
print()

if hasattr(model, "feature_names_in_"):
    print("Expected feature names:", list(model.feature_names_in_))
if hasattr(model, "n_features_in_"):
    print("Expected number of features:", model.n_features_in_)
if hasattr(model, "steps"):
    print("Pipeline steps:", model.steps)