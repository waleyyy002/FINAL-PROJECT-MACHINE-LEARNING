const form = document.querySelector('#prediction-form');
const errorMessage = document.querySelector('#form-error');
const emptyResult = document.querySelector('#empty-result');
const predictionResult = document.querySelector('#prediction-result');
const predictionLabel = document.querySelector('#prediction-label');
const probabilityValue = document.querySelector('#probability-value');
const probabilityMeter = document.querySelector('#probability-meter');
const resultCopy = document.querySelector('#result-copy');
const buttonLabel = document.querySelector('#button-label');
const resetButton = document.querySelector('#reset-button');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorMessage.textContent = '';
  buttonLabel.textContent = 'Assessing profile...';
  form.querySelector('button[type="submit"]').disabled = true;

  const values = Object.fromEntries(new FormData(form).entries());
  values.Tenure_Months = Number(values.Tenure_Months);
  values.Monthly_Charges = Number(values.Monthly_Charges);
  values.Total_Charges = Number(values.Total_Charges);
  values.CLTV = Number(values.CLTV);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(values)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'The assessment could not be completed.');
    const probability = Math.round(data.churn_probability * 100);
    predictionLabel.textContent = data.prediction;
    probabilityValue.textContent = `${probability}%`;
    probabilityMeter.style.width = `${probability}%`;
    resultCopy.textContent = data.prediction === 'Churn'
      ? 'This profile shows elevated churn risk. Consider a proactive retention touchpoint.'
      : 'The current customer profile shows a lower likelihood of churn.';
    emptyResult.classList.add('hidden');
    predictionResult.classList.remove('hidden');
  } catch (error) {
    errorMessage.textContent = error.message;
  } finally {
    buttonLabel.textContent = 'Run risk assessment';
    form.querySelector('button[type="submit"]').disabled = false;
  }
});

resetButton.addEventListener('click', () => {
  predictionResult.classList.add('hidden');
  emptyResult.classList.remove('hidden');
  probabilityMeter.style.width = '0';
  errorMessage.textContent = '';
});
