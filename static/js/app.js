(() => {
  const form = document.getElementById('forecast-form');
  const resultCard = document.getElementById('prediction-result');
  const scenarioSelect = document.getElementById('scenario_id');
  const scenarioDescription = document.getElementById('scenario-description');
  const scenarioPresets = window.SCENARIO_PRESETS || [];
  const scenarioMap = scenarioPresets.reduce((acc, scenario) => {
    acc[scenario.id] = scenario;
    return acc;
  }, {});

  const setResult = (title, message, status = 'idle') => {
    if (!resultCard) return;
    resultCard.classList.remove('success', 'error');
    if (status === 'success') resultCard.classList.add('success');
    if (status === 'error') resultCard.classList.add('error');
    resultCard.querySelector('h3').textContent = title;
    resultCard.querySelector('p:nth-of-type(2)')?.remove();
    const paragraph = document.createElement('p');
    paragraph.textContent = message;
    resultCard.appendChild(paragraph);
  };

  if (!form) return;

  const applyScenario = (scenarioId) => {
    const scenario = scenarioMap[scenarioId];
    if (!scenario) return;

    if (scenarioDescription) {
      scenarioDescription.textContent = scenario.description;
    }

    Object.entries(scenario.values).forEach(([key, value]) => {
      const input = form.elements.namedItem(key);
      if (input) {
        input.value = Number(value).toFixed(2);
      }
    });
  };

  if (scenarioSelect) {
    scenarioSelect.addEventListener('change', (event) => {
      applyScenario(event.target.value);
    });
    applyScenario(scenarioSelect.value);
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    setResult('Running forecast…', 'Crunching inputs with the trained XGBoost model.');

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const body = await response.json();

      if (!response.ok) {
        throw new Error(body.error || 'Forecast failed');
      }

      const mu = Number(body.prediction).toFixed(2);
      setResult('Projected Energy Required', `${mu} MU`, 'success');
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      setResult('Could not generate forecast', message, 'error');
    }
  });
})();
