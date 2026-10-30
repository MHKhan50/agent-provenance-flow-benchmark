# Roman Urdu quick guide

Yeh project agent ke tool-output provenance ko test karta hai: jab agent kisi external document ya tool se data leta hai aur us data ko copy, summarise, translate, extract ya merge karta hai, to kya source ka trust label aage bhi rehta hai?

## Research sawal
Kya field-level provenance ko transformations ke baad preserve karne se security behtar hoti hai, bina legitimate task ko zyada block kiye?

## Run
Terminal mein repo folder ke andar yeh command chalao:

```bash
python3 generate_dataset.py && python3 run_benchmark.py && python3 -m unittest discover -s tests -v
```

Koi pip install, internet, API key ya GPU nahi chahiye.

## Kya milega?
`outputs/` mein CSV results, JSON summary aur SVG graphs banenge.

Yeh synthetic simulator hai. Is mein real LLM ya real email/browser/tool action nahi chalta. Is liye results ko real-world agent security ka proof mat samajhna.
