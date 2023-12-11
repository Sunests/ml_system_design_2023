CREATE TABLE energy (
  class_id INTEGER PRIMARY KEY,
  class_name VARCHAR(100) NOT NULL,
  bzu VARCHAR(100) NOT NULL
);

CREATE TABLE prices (
  class_id INTEGER PRIMARY KEY,
  class_name VARCHAR(100) NOT NULL,
  price NUMERIC(10,2) NOT NULL
); 

INSERT INTO energy (class_id, class_name, bzu) VALUES
(1, 'алоэвера', 'БЖУ - 0,10/0,00/0,75'),
(2, 'банан', 'БЖУ - 1,50/0,92/21,80'),
(3, 'билимби', 'БЖУ - 1,00/0,00/4,00'),
(4, 'дыня', 'БЖУ - 0,84/0,19/8,16'),
(5, 'маниока', 'БЖУ - 1,36/ 0,28/ 38,06'),
(6, 'кокос', 'БЖУ - 3,33/33,49/15,23'),
(7, 'кукуруза', 'БЖУ - 3,27/ 1,18/ 18,70'),
(8, 'огурец', 'БЖУ - 0,65/0,11/2,16'),
(9, 'куркума', 'БЖУ - 7,83/9,68/64,93'),
(10, 'баклажан', 'БЖУ - 0,98/0,18/4,82'),
(11, 'галангал', 'БЖУ - 1,88/0,39/18,12'),
(12, 'имбирный', 'БЖУ - 1,82/0,75/17,77'),
(13, 'гуава', 'БЖУ - 2,55/0,95/14,32'),
(14, 'капуста', 'БЖУ - 4,28/0,93/8,75'),
(15, 'длинная фасоль', 'БЖУ - 1,83/0,34/3,38'),
(16, 'Манго', 'БЖУ - 0,82/ 0,38/ 14,98'),
(17, 'дыня', 'БЖУ - 0,54/0,15/7,86'),
(18, 'оранжевый', 'БЖУ - 0,94/0,12/8,35'),
(19, 'падди', 'БЖУ - 7,50/ 1,30/ 77,70'),
(20, 'папайя', 'БЖУ - 0,47/0,26/10,82'),
(21, 'пеперчили', 'БЖУ - 2.00/0.20/9.00'),
(22, 'ананас', 'БЖУ - 0,54/0,12/11,82'),
(23, 'помело', 'БЖУ - 0,76/0,04/6,68'),
(24, 'шалот', 'БЖУ - 1,20/0,10/16,80'),
(25, 'Соевые бобы', 'БЖУ - 36,49/ 18,63/ 30,16'),
(26, 'шпинат', 'БЖУ - 2,86/0,39/3,63'),
(27, 'батат', 'БЖУ - 1,57/0,05/17,41'),
(28, 'Табак', 'БЖУ - 16.00/0.00/0.00'),
(29, 'водяное яблоко', 'БЖУ - 0,60/0,20/13,50'),
(30, 'Арбуз', 'БЖУ - 0,61/0,15/7,55'),
(31, 'брокколи', 'БЖУ - 2,82/0,37/6,64'),
(32, 'шафран', 'БЖУ - 11,43/5,85/65,37');

INSERT INTO prices (class_id, class_name, price) VALUES
(1, 'алоэвера', 100),
(2, 'банан', 50),
(3, 'билимби', 200),
(4, 'дыня', 30),
(5, 'маниока', 10),
(6, 'кокос', 80),
(7, 'кукуруза', 20),
(8, 'огурец', 15),
(9, 'куркума', 500),
(10, 'баклажаны', 25),
(11, 'галангал', 300),
(12, 'имбирь', 100),
(13, 'гуава', 40),
(14, 'капуста', 200),
(15, 'длинная фасоль', 30),
(16, 'манго', 70),
(17, 'дыня', 25),
(18, 'оранжевый', 40),
(19, 'падди', 100),
(20, 'папайя', 60),
(21, 'пеперчили', 50),
(22, 'ананас', 30),
(23, 'помело', 50),
(24, 'шалот', 80),
(25, 'соевые бобы', 150),
(26, 'шпинат', 100),
(27, 'батат', 20),
(28, 'табак', 500),
(29, 'водяное яблоко', 40),
(30, 'арбуз', 30),
(31, 'брокколи', 1500),
(32, 'шафран', 5000);