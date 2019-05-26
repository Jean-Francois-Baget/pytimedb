# Résultats tests insertions

## Test 1 (10.000 insertions, max: 1000, proba: x)

```python
for i in range(100):
    results.append(test(10000, 1000, i/100))
```

![Resultat](/resultats/images/vlcsnap-2017-06-09-15h09m29s724.png)


## Test 2 (x * 500) insertions, max : 1000, proba : 0.8

```python
for i in range(100):
    results.append(test(500 * i, 1000, 0.8))
```

![Resultat](/resultats/images/Figure_1.png)

## Test 3 (x * 1000) insertions, max : 500, proba : 0.8

```python
for i in range(100):
    results.append(test(1000 * i, 500, 0.8))
```

![Resultat](/resultats/images/Figure_2.png)


