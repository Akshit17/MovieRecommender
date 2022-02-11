# Movie Recommender


Semantic Search based Movie Recommendation system. <br />
In contrast to traditional search methods, semantic search is a method of extracting relevant information from a large corpus of documents. <br />
This repository is an attempt to illustrate the same.


# Demo Gif
<img src="Assets/demo-recom-compress1.gif" width="900" height="500" />


## Technologies Used
- **Backend**:  Flask, Jina
- **Frontend**:  Html , CSS, Javascript , React.js

## How to Run Locally ?
- Clone the Repository
```
https://github.com/Akshit17/MovieRecommender.git
```
- Create a virtual environment 
``` 
virtualenv myenv 
```
   - For Linux
``` 
source ./myenv/bin/activate
```
   - For Windows
``` 
./myenv/Scripts/activate
```
- Install all the required packages with pip
 ```
 pip3 install -r requirements.txt
 ```

💢 Make sure that the dataset in `./data_finalize/movies_metadata.csv` is **indexed** by running `jina_app.py` with line 55 **Uncommented**. <br/>
         Dont Forget to **Comment it again** after indexing to **avoid indexing everytime** a query passed when integrating it with Flask app.💢

- Run `jina_app.py`(_Again after indexing the data from previous step_) to serve **Flow as a service** . {Note down the address at which it is served from CLI for eg. "0.0.0.0:34567"}
```
  python3 jina_app.py 
  ```
  
💢Make Sure in `app.py` line 44 `url` is same as where Flow is being served so that Flask app and Jina can communicate💢
<br/>

- Run the Flask Application `app.py` in another terminal alongside `jina_app.py` to get the web applcation running at "localhost:port"
 ```
  python3 app.py
  ```
  <br/>
  <br/>
  <br/>
  
  🍙 🍟 You've made it to the bottom 🧁 🍕
