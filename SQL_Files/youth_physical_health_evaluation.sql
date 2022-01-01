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
-- Table structure for table `physical_health_evaluation`
--

DROP TABLE IF EXISTS `physical_health_evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `physical_health_evaluation` (
  `physicalShareCode` int NOT NULL,
  `day` varchar(100) DEFAULT NULL,
  `month` varchar(100) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `height` varchar(255) DEFAULT NULL,
  `temperature` varchar(255) DEFAULT NULL,
  `heartRate` int DEFAULT NULL,
  `bloodPressure` varchar(255) DEFAULT NULL,
  `respiratoryRate` int DEFAULT NULL,
  `pedSIN` int DEFAULT NULL,
  `youthName` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`physicalShareCode`),
  KEY `fk_PHE` (`pedSIN`),
  CONSTRAINT `fk_PHE` FOREIGN KEY (`pedSIN`) REFERENCES `pediatrician` (`SIN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `physical_health_evaluation`
--

LOCK TABLES `physical_health_evaluation` WRITE;
/*!40000 ALTER TABLE `physical_health_evaluation` DISABLE KEYS */;
INSERT INTO `physical_health_evaluation` VALUES (5,'30','12',2021,62,'1.7','37.1',80,'120/78',14,223456789,'Melissa'),(6,'30','12',2021,71,'1.6','37.2',92,'119/79',16,223456789,'Alex'),(9,'4','10',2021,68,'1.5','37.3',76,'120/79',15,223456789,'Luke');
/*!40000 ALTER TABLE `physical_health_evaluation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-31 23:45:59
