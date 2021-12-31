-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: youth
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `symptoms`
--

DROP TABLE IF EXISTS `symptoms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `symptoms` (
  `mentalShareCode` int NOT NULL,
  `symptom` varchar(255) NOT NULL,
  `severity` int NOT NULL,
  `symptom2` varchar(255) DEFAULT NULL,
  `severity2` int DEFAULT NULL,
  `symptom3` varchar(255) DEFAULT NULL,
  `severity3` int DEFAULT NULL,
  `symptom4` varchar(255) DEFAULT NULL,
  `severity4` int DEFAULT NULL,
  `symptom5` varchar(255) DEFAULT NULL,
  `severity5` int DEFAULT NULL,
  `symptom6` varchar(255) DEFAULT NULL,
  `severity6` int DEFAULT NULL,
  `symptom7` varchar(255) DEFAULT NULL,
  `severity7` int DEFAULT NULL,
  `symptom8` varchar(255) DEFAULT NULL,
  `severity8` int DEFAULT NULL,
  `symptom9` varchar(255) DEFAULT NULL,
  `severity9` int DEFAULT NULL,
  `symptom10` varchar(255) DEFAULT NULL,
  `severity10` int DEFAULT NULL,
  PRIMARY KEY (`mentalShareCode`,`symptom`,`severity`),
  CONSTRAINT `fk_SYMPTOMS` FOREIGN KEY (`mentalShareCode`) REFERENCES `mental_health_evaluation` (`mentalShareCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `symptoms`
--

LOCK TABLES `symptoms` WRITE;
/*!40000 ALTER TABLE `symptoms` DISABLE KEYS */;
INSERT INTO `symptoms` VALUES (2,'Depression',9,'Anxiety',8,'Lethargy',7,'Excessive Fear',5,'Excessive Worrying',9,'Extreme Mood Changes',10,'Trouble Sleeping',7,'Trouble Concentrating',4,'Loss of Interest',3,'Appetite',1),(4,'Depression',4,'Anxiety',6,'Lethargy',2,'Excessive Fear',1,'Excessive Worrying',2,'Extreme Mood Changes',6,'Trouble Sleeping',9,'Trouble Concentrating',10,'Loss of Interest',4,'Appetite',3);
/*!40000 ALTER TABLE `symptoms` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-31 16:49:39
