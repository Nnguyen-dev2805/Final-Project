# Revenue Forecast Streamlit Demo

Demo nay dung 3 artifact:

- `app/artifacts/m5_model.joblib`
- `app/artifacts/maven_model.joblib`
- `app/artifacts/weather_sales_model.joblib`

## Tao moi environment

```bash
python3 -m venv --system-site-packages .venv-streamlit-demo
source .venv-streamlit-demo/bin/activate
python -m pip install --upgrade pip
python -m pip install -r app/requirements.txt
```

## Train artifact

```bash
source .venv-streamlit-demo/bin/activate
python app/train_artifacts.py
```

Train rieng tung model:

```bash
python app/train_artifacts.py --models m5
python app/train_artifacts.py --models maven
python app/train_artifacts.py --models weather
```

## Chay Streamlit

```bash
source .venv-streamlit-demo/bin/activate
streamlit run app/streamlit_app.py
```

Mac dinh app se dung cac dong mau that tu test set duoc luu trong artifact, sau do cho chinh mot so bien numeric de demo kich ban du doan.
