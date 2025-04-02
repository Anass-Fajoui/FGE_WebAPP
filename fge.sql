-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: fge
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `appartenir`
--

DROP TABLE IF EXISTS `appartenir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appartenir` (
  `Cellule_id` int NOT NULL,
  `Club_id` int NOT NULL,
  PRIMARY KEY (`Cellule_id`,`Club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appartenir`
--

LOCK TABLES `appartenir` WRITE;
/*!40000 ALTER TABLE `appartenir` DISABLE KEYS */;
INSERT INTO `appartenir` VALUES (1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3),(4,1),(4,2),(4,3),(5,1),(5,2),(5,3),(6,1),(6,2),(6,3);
/*!40000 ALTER TABLE `appartenir` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cellule`
--

DROP TABLE IF EXISTS `cellule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cellule` (
  `Cellule_id` int NOT NULL AUTO_INCREMENT,
  `Cellule_nom` varchar(100) NOT NULL,
  PRIMARY KEY (`Cellule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cellule`
--

LOCK TABLES `cellule` WRITE;
/*!40000 ALTER TABLE `cellule` DISABLE KEYS */;
INSERT INTO `cellule` VALUES (1,'Média'),(2,'Technique'),(3,'Logistique'),(4,'Prospection'),(5,'Rédaction'),(6,'Sponsoring');
/*!40000 ALTER TABLE `cellule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `club`
--

DROP TABLE IF EXISTS `club`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `club` (
  `Club_id` int NOT NULL,
  `Club_Nom` varchar(100) NOT NULL,
  PRIMARY KEY (`Club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `club`
--

LOCK TABLES `club` WRITE;
/*!40000 ALTER TABLE `club` DISABLE KEYS */;
INSERT INTO `club` VALUES (1,'FGE_inpt'),(2,'FGE_ensias'),(3,'FGE_insea');
/*!40000 ALTER TABLE `club` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employe_rh`
--

DROP TABLE IF EXISTS `employe_rh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employe_rh` (
  `RH_id` int NOT NULL AUTO_INCREMENT,
  `RH_Nom` varchar(50) NOT NULL,
  `RH_Prenom` varchar(50) NOT NULL,
  `RH_Email` varchar(100) NOT NULL,
  `Entreprise_id` int DEFAULT NULL,
  PRIMARY KEY (`RH_id`),
  UNIQUE KEY `RH_Email` (`RH_Email`),
  KEY `employe_rh_fk1` (`Entreprise_id`),
  CONSTRAINT `employe_rh_fk1` FOREIGN KEY (`Entreprise_id`) REFERENCES `entreprise` (`Entreprise_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employe_rh`
--

LOCK TABLES `employe_rh` WRITE;
/*!40000 ALTER TABLE `employe_rh` DISABLE KEYS */;
INSERT INTO `employe_rh` VALUES (1,'El Amrani','Youssef','youssef.elamrani@orange.com',1),(2,'Bennani','Sanae','sanae.bennani@orange.com',1),(3,'El Idrissi','Khadija','khadija.elidrissi@inwi.ma',2),(4,'Othmani','Hamza','hamza.othmani@inwi.ma',2),(5,'Maaroufi','Mohammed','mohammed.maaroufi@oncf.ma',3),(6,'Zerouali','Fatima','fatima.zerouali@oncf.ma',3),(7,'Bouchikhi','Rachid','rachid.bouchikhi@attijariwafabank.com',4),(8,'Lahlou','Nawal','nawal.lahlou@attijariwafabank.com',4),(9,'Skalli','Meryem','meryem.skalli@dxc.com',5),(10,'Jabri','Anas','anas.jabri@dxc.com',5),(11,'El Fassi','Imane','imane.elfassi@bmce.ma',6),(12,'Rahmani','Omar','omar.rahmani@bmce.ma',6),(13,'Chraibi','Salma','salma.chraibi@deloitte.com',7),(14,'Moulay','Zakaria','zakaria.moulay@deloitte.com',7),(15,'Touhami','Khalid','khalid.touhami@leyton.com',8),(16,'Kabbaj','Leila','leila.kabbaj@leyton.com',8),(17,'Sefrioui','Amina','amina.sefrioui@oracle.com',9),(18,'Faqihi','Younes','younes.faqihi@oracle.com',9);
/*!40000 ALTER TABLE `employe_rh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entreprise`
--

DROP TABLE IF EXISTS `entreprise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entreprise` (
  `Entreprise_id` int NOT NULL AUTO_INCREMENT,
  `Ent_Nom` varchar(100) NOT NULL,
  PRIMARY KEY (`Entreprise_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entreprise`
--

LOCK TABLES `entreprise` WRITE;
/*!40000 ALTER TABLE `entreprise` DISABLE KEYS */;
INSERT INTO `entreprise` VALUES (1,'Orange'),(2,'Inwi'),(3,'ONCF'),(4,'Attijariwafa Bank'),(5,'DXC'),(6,'BMCE'),(7,'Deloitte'),(8,'Leyton'),(9,'Oracle'),(22,'anassinc');
/*!40000 ALTER TABLE `entreprise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evenement`
--

DROP TABLE IF EXISTS `evenement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evenement` (
  `Year` int NOT NULL,
  `Club_id` int DEFAULT NULL,
  PRIMARY KEY (`Year`),
  KEY `Club_id` (`Club_id`),
  CONSTRAINT `evenement_ibfk_1` FOREIGN KEY (`Club_id`) REFERENCES `club` (`Club_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evenement`
--

LOCK TABLES `evenement` WRITE;
/*!40000 ALTER TABLE `evenement` DISABLE KEYS */;
INSERT INTO `evenement` VALUES (2024,1),(2022,2),(2023,3);
/*!40000 ALTER TABLE `evenement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membre`
--

DROP TABLE IF EXISTS `membre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membre` (
  `Membre_id` int NOT NULL AUTO_INCREMENT,
  `Nom` varchar(50) NOT NULL,
  `Prenom` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Role` varchar(50) DEFAULT NULL,
  `Club_id` int DEFAULT NULL,
  PRIMARY KEY (`Membre_id`),
  UNIQUE KEY `Email` (`Email`),
  KEY `Club_id` (`Club_id`),
  CONSTRAINT `membre_ibfk_1` FOREIGN KEY (`Club_id`) REFERENCES `club` (`Club_id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membre`
--

LOCK TABLES `membre` WRITE;
/*!40000 ALTER TABLE `membre` DISABLE KEYS */;
INSERT INTO `membre` VALUES (1,'El Amrani','Yassine','yassine.elamrani@example.com','Président',1),(2,'Ben Ali','Rachid','rachid.benali@example.com','Secrétaire Général',1),(3,'Amine','Sami','sami.amine@example.com','Vice-Président',1),(4,'Tazi','Sofia','sofia.tazi@example.com','Trésorier',1),(5,'Chouaib','Aziz','aziz.chouaib@example.com','Président',2),(6,'Ouladi','Sara','sara.ouladi@example.com','Secrétaire Général',2),(7,'Mouline','Amal','amal.mouline@example.com','Vice-Président',2),(8,'El Hachimi','Khalid','khalid.elhachimi@example.com','Trésorier',2),(9,'Ait Ben Ali','Fatima','fatima.aitbenali@example.com','Président',3),(10,'El Fassi','Hassan','hassan.elfassi@example.com','Secrétaire Général',3),(11,'Boujbar','Mouna','mouna.boujbar@example.com','Vice-Président',3),(12,'Chami','Youssef','youssef.chami@example.com','Trésorier',3),(13,'Bennani','Ali','ali.bennani@example.com','Membre',1),(14,'El Idrissi','Samira','samira.elidrissi@example.com','Membre',1),(15,'El Khatib','Youssef','youssef.elkhatib@example.com','Membre',1),(16,'Ouladsadiq','Mohammed','mohammed.ouladsadiq@example.com','Membre',1),(17,'Rachidi','Imane','imane.rachidi@example.com','Membre',1),(18,'Azouzi','Meryem','meryem.azouzi@example.com','Membre',1),(19,'Hicham','Saber','hicham.saber@example.com','Membre',1),(20,'Moulay','Omar','omar.moulay@example.com','Membre',1),(21,'Moulay','Khalil','khalil.moulay@example.com','Membre',1),(22,'Benyoussef','Imane','imane.benyoussef@example.com','Membre',1),(23,'El Khalil','Said','said.elkhalil@example.com','Membre',1),(24,'Khalfi','Latifa','latifa.khalfi@example.com','Membre',1),(25,'Tazi','Rachid','rachid.tazi@example.com','Membre',2),(26,'Moussa','Mouna','mouna.moussa@example.com','Membre',2),(27,'El Hadi','Ahmed','ahmed.elhadi@example.com','Membre',2),(28,'El Yousfi','Khaled','khaled.elyousfi@example.com','Membre',2),(29,'Benhamida','Siham','siham.benhamida@example.com','Membre',2),(30,'Kouta','Fatima','fatima.kouta@example.com','Membre',2),(31,'Jabiri','Yassir','yassir.jabiri@example.com','Membre',2),(32,'El Attar','Sanae','sanae.elattar@example.com','Membre',2),(33,'El Hariri','Rachida','rachida.elhariri@example.com','Membre',2),(34,'Tariq','Amina','amina.tariq@example.com','Membre',2),(35,'Bourkia','Ibrahim','ibrahim.bourkia@example.com','Membre',2),(36,'Naciri','Fouad','fouad.naciri@example.com','Membre',2),(37,'El Alami','Rachid','rachid.elalami@example.com','Membre',3),(38,'Benkirane','Mouhammad','mouhammad.benkirane@example.com','Membre',3),(39,'Aouad','Khalil','khalil.aouad@example.com','Membre',3),(40,'Chouhal','Amina','amina.chouhal@example.com','Membre',3),(41,'Boulahya','Mouad','mouad.boulahya@example.com','Membre',3),(42,'El Ouafi','Latifa','latifa.elouafi@example.com','Membre',3),(43,'Ouazzani','Imane','imane.ouazzani@example.com','Membre',3),(44,'Tazi','Fouad','fouad.tazi@example.com','Membre',3),(45,'Berrada','Hassan','hassan.berrada@example.com','Membre',3),(46,'Bakkali','Ibtissam','ibtissam.bakkali@example.com','Membre',3),(47,'Mouffok','Yassir','yassir.mouffok@example.com','Membre',3),(48,'Benjelloun','Nadia','nadia.benjelloun@example.com','Membre',3);
/*!40000 ALTER TABLE `membre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participant`
--

DROP TABLE IF EXISTS `participant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `participant` (
  `Participant_id` int NOT NULL AUTO_INCREMENT,
  `P_Nom` varchar(50) NOT NULL,
  `P_Prenom` varchar(50) NOT NULL,
  `P_Email` varchar(100) NOT NULL,
  PRIMARY KEY (`Participant_id`),
  UNIQUE KEY `P_Email` (`P_Email`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participant`
--

LOCK TABLES `participant` WRITE;
/*!40000 ALTER TABLE `participant` DISABLE KEYS */;
INSERT INTO `participant` VALUES (1,'El Khatib','Karim','karim.elkhatib@gmail.com'),(2,'Bouchaib','Mouna','mouna.bouchaib@gmail.com'),(3,'Alaoui','Yassine','yassine.alaoui@gmail.com'),(4,'Fadil','Sara','sara.fadil@gmail.com'),(5,'Benchekroun','Hamza','hamza.benchekroun@gmail.com'),(6,'Naimi','Aya','aya.naimi@gmail.com'),(7,'El Mansouri','Rachid','rachid.elmansouri@gmail.com'),(8,'Tazi','Soukaina','soukaina.tazi@gmail.com'),(9,'Chafik','Anas','anas.chafik@gmail.com'),(10,'El Idrissi','Nada','nada.elidrissi@gmail.com'),(11,'Hammoudi','Mohammed','mohammed.hammoudi@gmail.com'),(12,'Slaoui','Laila','laila.slaoui@gmail.com'),(13,'Bennis','Omar','omar.bennis@gmail.com'),(14,'Amrani','Hiba','hiba.amrani@gmail.com'),(15,'Berrada','Imane','imane.berrada@gmail.com'),(16,'El Fassi','Youssef','youssef.elfassi@gmail.com'),(17,'Kabbaj','Salma','salma.kabbaj@gmail.com'),(18,'Maalem','Zineb','zineb.maalem@gmail.com');
/*!40000 ALTER TABLE `participant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `postuler`
--

DROP TABLE IF EXISTS `postuler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `postuler` (
  `Participant_id` int NOT NULL,
  `RH_id` int NOT NULL,
  `Entreprise_id` int NOT NULL,
  `Year` int NOT NULL,
  `Poste` varchar(100) DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `postuler`
--

LOCK TABLES `postuler` WRITE;
/*!40000 ALTER TABLE `postuler` DISABLE KEYS */;
INSERT INTO `postuler` VALUES (1,1,1,2024,'software engineer',1),(2,2,1,2024,'data scientist',2),(3,3,2,2024,'data engineer',3),(4,4,2,2024,'data analyst',4),(5,5,3,2024,'software architect',5),(6,6,3,2024,'cloud engineer',6),(7,7,4,2023,'network engineer',7),(8,8,4,2023,'test engineer',8),(9,9,5,2023,'software engineer',9),(10,10,5,2023,'data scientist',10),(11,11,6,2023,'data engineer',11),(12,12,6,2023,'data analyst',12),(13,13,7,2022,'software architect',13),(14,14,7,2022,'cloud engineer',14),(15,15,8,2022,'network engineer',15),(16,16,8,2022,'test engineer',16),(17,17,9,2022,'software engineer',17),(18,18,9,2022,'data scientist',18);
/*!40000 ALTER TABLE `postuler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `s_inscrire`
--

DROP TABLE IF EXISTS `s_inscrire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `s_inscrire` (
  `Membre_id` int NOT NULL,
  `Cellule_id` int NOT NULL,
  `EstChef` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`Membre_id`,`Cellule_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `s_inscrire`
--

LOCK TABLES `s_inscrire` WRITE;
/*!40000 ALTER TABLE `s_inscrire` DISABLE KEYS */;
INSERT INTO `s_inscrire` VALUES (13,1,0),(14,1,1),(15,2,0),(16,2,1),(17,3,0),(18,3,1),(19,4,0),(20,4,1),(21,5,0),(22,5,1),(23,6,0),(24,6,1),(25,1,0),(26,1,1),(27,2,0),(28,2,1),(29,3,0),(30,3,1),(31,4,0),(32,4,1),(33,5,0),(34,5,1),(35,6,0),(36,6,1),(37,1,0),(38,1,1),(39,2,0),(40,2,1),(41,3,0),(42,3,1),(43,4,0),(44,4,1),(45,5,0),(46,5,1),(47,6,0),(48,6,1);
/*!40000 ALTER TABLE `s_inscrire` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsoriser`
--

DROP TABLE IF EXISTS `sponsoriser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsoriser` (
  `Year` int NOT NULL,
  `Entreprise_id` int NOT NULL,
  `Sponsor_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Year`,`Entreprise_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsoriser`
--

LOCK TABLES `sponsoriser` WRITE;
/*!40000 ALTER TABLE `sponsoriser` DISABLE KEYS */;
INSERT INTO `sponsoriser` VALUES (2022,7,'gold'),(2022,8,'silver'),(2022,9,'platinium'),(2023,4,'gold'),(2023,5,'silver'),(2023,6,'platinium'),(2024,1,'gold'),(2024,2,'silver'),(2024,3,'platinium'),(2024,22,'gold');
/*!40000 ALTER TABLE `sponsoriser` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-14 19:32:40
