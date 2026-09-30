# Evaluation: keyword vs semantic vs hybrid search

10,000 movies, 38 test queries, model `BAAI/bge-small-en-v1.5`.

| Query type | Queries | keyword Hit@5 | semantic Hit@5 | hybrid Hit@5 | keyword MRR | semantic MRR | hybrid MRR |
|---|---|---|---|---|---|---|---|
| ALL | 38 | 55% | 66% | 66% | 0.51 | 0.49 | 0.55 |
| describe the idea | 32 | 47% | 59% | 59% | 0.45 | 0.45 | 0.51 |
| exact names | 6 | 100% | 100% | 100% | 0.83 | 0.69 | 0.81 |

## Every query (rank of the correct movie, 1 is best)

| Query | Correct movie | Keyword | Semantic | Hybrid |
|---|---|---|---|---|
| a man is stuck reliving the same day again and again | Groundhog Day | >100 | 20 | 39 |
| thieves steal secrets by sneaking into people's dreams | Inception | >100 | >100 | >100 |
| a guy slowly realises his whole life is secretly being broadcast as a TV show | The Truman Show | 19 | >100 | 36 |
| a lonely little robot cleans up an abandoned Earth covered in trash | WALL-E | 1 | 1 | 1 |
| a young boy forgotten at home by his family has to protect the house from two crooks | Home Alone | >100 | >100 | >100 |
| an astronaut left behind on another planet has to grow his own food to survive | The Martian | 6 | 1 | 1 |
| a worried father fish crosses the ocean to find his missing son | Finding Nemo | 7 | 13 | 2 |
| a girl's feelings are little characters living inside her head | Inside Out | >100 | 3 | 11 |
| a child who can't read properly is called lazy until a teacher realises he has a learning disorder | Taare Zameen Par | >100 | 1 | 13 |
| an alien lands on earth and starts questioning why people follow religion | PK | 1 | 1 | 1 |
| a murdered man comes back as a tiny insect to take revenge on his killer | Makkhi | >100 | >100 | >100 |
| a father hides all the evidence to protect his family after his daughter accidentally kills a boy | Drishyam | >100 | >100 | >100 |
| a scientist builds a humanoid robot that falls in love with the scientist's girlfriend | Robot | 5 | 1 | 1 |
| a gangster pretends to be a doctor in training so his parents think he is respectable | Munna Bhai M.B.B.S. | 39 | 3 | 3 |
| a woman goes on her honeymoon trip alone after her fiance calls off the wedding | Queen | 26 | >100 | 56 |
| a housewife secretly takes language classes after her family mocks her for her poor English | English Vinglish | 1 | 3 | 2 |
| a man with short-term memory loss tracks down the person who murdered his wife | Memento | >100 | 14 | 35 |
| a child who can see ghosts is treated by a psychologist | The Sixth Sense | 1 | 30 | 2 |
| a lawyer is magically unable to tell a single lie for a whole day | Liar Liar | 1 | 4 | 1 |
| a mother and her teenage daughter wake up in each other's bodies | Freaky Friday | 6 | >100 | 17 |
| a traveller gets stuck living in an airport for months because his passport becomes invalid | The Terminal | 1 | 4 | 1 |
| a board game brings wild jungle animals into a small town | Jumanji | 1 | 98 | 10 |
| an inventor accidentally shrinks his children to the size of insects | Honey, I Shrunk the Kids | 8 | 44 | 6 |
| a divorced dad disguises himself as an elderly nanny so he can see his kids | Mrs. Doubtfire | 46 | 5 | 4 |
| after a plane crash a man survives completely alone on an island for years | Cast Away | 8 | 1 | 2 |
| a rat who dreams of becoming a chef in a fancy restaurant | Ratatouille | 1 | 1 | 1 |
| a pig raised by a sheepdog learns to herd sheep | Babe | 1 | 1 | 1 |
| a pilot makes an emergency landing on a river after birds hit the engines | Sully | 1 | 1 | 1 |
| poor villagers bet against British officers in a cricket match to escape heavy taxes | Lagaan: Once Upon a Time in India | 1 | 1 | 1 |
| a lonely man falls in love with the voice of his computer's operating system | Her | 1 | 1 | 1 |
| a bus is rigged to explode if it drops below fifty miles per hour | Speed | 1 | 1 | 1 |
| a man keeps waking up on a train minutes before a bomb goes off | Source Code | 3 | 3 | 1 |
| Marty McFly DeLorean Doc Brown | Back to the Future | 2 | 3 | 3 |
| Hannibal Lecter Clarice Starling | The Silence of the Lambs | 2 | 2 | 2 |
| Simba Mufasa Scar | The Lion King | 1 | 1 | 1 |
| Rancho Farhan Raju | 3 Idiots | 1 | 1 | 1 |
| Jack Dawson Rose DeWitt Bukater | Titanic | 1 | 3 | 1 |
| John McClane Nakatomi Plaza | Die Hard | 1 | 1 | 1 |
