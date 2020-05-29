## Usage:

------------
```python
import web_app.utils.MLModel
tr = MLModel.Transformer()
model = MLModel.load_pickle("path/to/picklefile")
negative = ['negative']
ignore = ['index','id']
user_transformed = tr.transform(pd.dataframe({'name':str,
                                              'race':str,
                                              'flavors':list,
                                              'negative':list
                                              'positive':list,
                                              'medical':list,
                                              'description':str,
                                              'preference':list
                                              }),
                                negative,
                                ignore)
pred = model.predict(user_transformed)
pred[1]

```
<p>

the `ignore` keyword is a list of column names that should be excluded from the model.

the `negative` keyword is a list of column names that should have a negitive effect
on the recomendation, for init training we used:

</p>

