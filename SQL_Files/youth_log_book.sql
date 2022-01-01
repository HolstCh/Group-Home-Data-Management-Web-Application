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
-- Table structure for table `log_book`
--

DROP TABLE IF EXISTS `log_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_book` (
  `logShareCode` int NOT NULL,
  `day` varchar(100) DEFAULT NULL,
  `month` varchar(100) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `event` varchar(255) DEFAULT NULL,
  `behaviour` varchar(255) DEFAULT NULL,
  `actionsTaken` varchar(255) DEFAULT NULL,
  `YSIN` int DEFAULT NULL,
  `youthName` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`logShareCode`),
  KEY `fk_LOG_BOOK` (`YSIN`),
  CONSTRAINT `fk_LOG_BOOK` FOREIGN KEY (`YSIN`) REFERENCES `youth_worker` (`SIN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_book`
--

LOCK TABLES `log_book` WRITE;
/*!40000 ALTER TABLE `log_book` DISABLE KEYS */;
INSERT INTO `log_book` VALUES (1,'28','12',2021,'I had asked Alex multiple times to do his homework. He responded with a temper tantrum and started throwing his toys at me.','Aggressive','I had removed all toys from the area and told him that he could not play with his toys until he had completed all of his homework.',123456789,'Alex'),(3,'30','12',2021,'Melissa displayed proper etiquette when we had supper last night. She has made substantial progress considering how rude she was in the past.','Polite','I rewarded her for learning manners at the supper table by giving her extra dessert. She did not expect the reward and seemed thankful.',123456789,'Melissa');
/*!40000 ALTER TABLE `log_book` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-31 16:49:37
