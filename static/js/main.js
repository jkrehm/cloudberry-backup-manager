Array.from(document.querySelectorAll('select[data-control]')).forEach(el => {
  el.addEventListener('change', e => {
    const el = e.currentTarget;
    const control = el.dataset.control;
    const selected = el.options[el.selectedIndex].value;

    Array.from(document.querySelectorAll(`[data-related=${control}]`)).forEach(el => {
      const values = JSON.parse(el.dataset.values);
      el.classList.toggle('is-hidden', !values.includes(selected));
    });
  });
});

Array.from(document.querySelectorAll('input[data-control][type="checkbox"]')).forEach(el => {
  el.addEventListener('change', e => {
    const el = e.currentTarget;
    const control = el.dataset.control;
    const checked = el.checked;

    Array.from(document.querySelectorAll(`[data-related=${control}]`)).forEach(el => {
      el.classList.toggle('is-hidden', !checked);
    });
  });
});

