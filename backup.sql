-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: attendance_db
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance_records`
--

DROP TABLE IF EXISTS `attendance_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `session_id` int NOT NULL,
  `student_id` int NOT NULL,
  `unit_id` int NOT NULL,
  `marked_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('present','manual') DEFAULT 'present',
  PRIMARY KEY (`record_id`),
  UNIQUE KEY `session_id` (`session_id`,`student_id`),
  KEY `idx_session` (`session_id`),
  KEY `idx_student` (`student_id`),
  KEY `idx_unit` (`unit_id`),
  KEY `idx_marked_at` (`marked_at`),
  CONSTRAINT `attendance_records_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`session_id`) ON DELETE CASCADE,
  CONSTRAINT `attendance_records_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `attendance_records_ibfk_3` FOREIGN KEY (`unit_id`) REFERENCES `units` (`unit_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_records`
--

LOCK TABLES `attendance_records` WRITE;
/*!40000 ALTER TABLE `attendance_records` DISABLE KEYS */;
INSERT INTO `attendance_records` VALUES (1,14,2,1,'2026-07-23 16:53:54','present'),(2,15,2,1,'2026-07-23 17:53:37','present'),(3,16,2,1,'2026-07-23 18:06:36','present'),(4,19,2,1,'2026-07-28 12:22:44','present'),(5,20,2,1,'2026-07-28 12:31:15','present'),(6,21,2,1,'2026-07-28 12:39:27','present'),(7,23,2,1,'2026-07-28 14:08:13','present');
/*!40000 ALTER TABLE `attendance_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(100) NOT NULL,
  `detail` text,
  `ip_address` varchar(45) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_action` (`action`),
  KEY `idx_timestamp` (`timestamp`),
  CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=159 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
INSERT INTO `audit_log` VALUES (1,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 11:18:33'),(2,3,'logout','User logged out','127.0.0.1','2026-06-07 11:18:49'),(3,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 11:19:28'),(4,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 11:43:55'),(5,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 11:53:53'),(6,5,'logout','User logged out','127.0.0.1','2026-06-07 12:06:54'),(7,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 12:07:01'),(8,5,'logout','User logged out','127.0.0.1','2026-06-07 12:10:37'),(9,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 12:10:41'),(10,5,'login','User admin@example.com logged in','192.168.0.103','2026-06-07 12:12:15'),(11,5,'logout','User logged out','192.168.0.103','2026-06-07 12:33:13'),(12,5,'login','User admin@example.com logged in','192.168.0.103','2026-06-07 12:33:19'),(13,5,'logout','User logged out','192.168.0.103','2026-06-07 12:37:46'),(14,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 12:40:10'),(15,5,'logout','User logged out','127.0.0.1','2026-06-07 12:43:16'),(16,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 12:43:20'),(17,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 13:01:38'),(18,5,'login','User admin@example.com logged in','192.168.0.103','2026-06-07 13:03:43'),(19,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 13:06:04'),(20,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 13:12:24'),(21,5,'login','User admin@example.com logged in','192.168.0.103','2026-06-07 13:47:18'),(22,3,'logout','User logged out','127.0.0.1','2026-06-07 13:52:48'),(23,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 13:55:27'),(24,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-07 14:02:11'),(25,3,'session_started','Session started for unit 2','127.0.0.1','2026-06-07 14:09:17'),(26,3,'session_started','Session started for unit 25','127.0.0.1','2026-06-07 14:14:15'),(27,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 14:14:29'),(28,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 14:14:38'),(29,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 14:23:01'),(30,5,'logout','User logged out','127.0.0.1','2026-06-07 14:26:24'),(31,4,'login','User james@example.com logged in','127.0.0.1','2026-06-07 14:28:51'),(32,4,'session_started','Session started for unit 24','127.0.0.1','2026-06-07 14:29:01'),(33,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-07 14:35:32'),(34,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 14:36:50'),(35,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 14:46:19'),(36,4,'login','User james@example.com logged in','127.0.0.1','2026-06-07 14:47:14'),(37,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 14:51:45'),(38,3,'logout','User logged out','127.0.0.1','2026-06-07 14:53:42'),(39,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-07 14:53:46'),(40,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-08 19:45:50'),(41,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-08 19:46:07'),(42,3,'session_ended','Session 1 ended','127.0.0.1','2026-06-08 19:49:32'),(43,3,'session_ended','Session 2 ended','127.0.0.1','2026-06-08 19:49:34'),(44,3,'session_ended','Session 3 ended','127.0.0.1','2026-06-08 19:49:36'),(45,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-08 19:49:39'),(46,3,'session_ended','Session 5 ended','127.0.0.1','2026-06-08 19:52:34'),(47,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-08 19:52:37'),(48,3,'session_ended','Session 6 ended','127.0.0.1','2026-06-08 19:54:26'),(49,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-08 19:54:30'),(50,3,'logout','User logged out','127.0.0.1','2026-06-08 19:56:43'),(51,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-08 19:56:48'),(52,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-10 10:04:13'),(53,3,'session_ended','Session 7 ended','127.0.0.1','2026-06-10 10:04:18'),(54,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-10 10:04:21'),(55,3,'logout','User logged out','127.0.0.1','2026-06-10 10:16:34'),(56,2,'login','User bob@example.com logged in','127.0.0.1','2026-06-10 10:17:56'),(57,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-10 10:54:13'),(58,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-10 10:54:14'),(59,3,'session_ended','Session 8 ended','127.0.0.1','2026-06-10 10:54:23'),(60,3,'logout','User logged out','127.0.0.1','2026-06-10 10:57:21'),(61,2,'login','User bob@example.com logged in','127.0.0.1','2026-06-10 11:02:41'),(62,2,'login','User bob@example.com logged in','127.0.0.1','2026-06-10 11:04:12'),(63,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-10 11:07:31'),(64,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-10 11:07:48'),(65,3,'session_ended','Session 9 ended','127.0.0.1','2026-06-10 11:12:41'),(66,3,'session_started','Session started for unit 2','127.0.0.1','2026-06-10 11:12:47'),(67,3,'session_ended','Session 10 ended','127.0.0.1','2026-06-10 11:14:22'),(68,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-10 11:14:25'),(69,3,'session_ended','Session 11 ended','127.0.0.1','2026-06-10 11:18:48'),(70,3,'logout','User logged out','127.0.0.1','2026-06-10 11:18:51'),(71,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-10 11:18:55'),(72,2,'enrolled','Enrolled in unit 1','127.0.0.1','2026-06-10 11:23:45'),(73,2,'login','User bob@example.com logged in','127.0.0.1','2026-06-11 07:52:29'),(74,2,'logout','User logged out','127.0.0.1','2026-06-11 07:53:01'),(75,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-11 07:53:05'),(76,3,'logout','User logged out','127.0.0.1','2026-06-11 09:28:50'),(77,2,'login','User bob@example.com logged in','127.0.0.1','2026-06-11 09:28:55'),(78,2,'logout','User logged out','127.0.0.1','2026-06-11 09:31:23'),(79,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-11 09:31:31'),(80,3,'STUDENT_NOTIFIED','Notified student 2 for unit 1','127.0.0.1','2026-06-11 09:32:33'),(81,2,'login','User bob@example.com logged in','127.0.0.1','2026-06-11 09:32:51'),(82,2,'login','User bob@example.com logged in','127.0.0.1','2026-06-17 04:58:12'),(83,2,'logout','User logged out','127.0.0.1','2026-06-17 04:58:42'),(84,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-17 04:58:47'),(85,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-17 04:59:29'),(86,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-17 04:59:39'),(87,3,'session_ended','Session 12 ended','127.0.0.1','2026-06-17 05:00:41'),(88,3,'login','User sarah@example.com logged in','127.0.0.1','2026-06-17 21:35:33'),(89,3,'session_started','Session started for unit 1','127.0.0.1','2026-06-17 21:36:13'),(90,3,'logout','User logged out','127.0.0.1','2026-06-17 21:53:42'),(91,5,'login','User admin@example.com logged in','127.0.0.1','2026-06-17 21:53:57'),(92,5,'login','User admin@example.com logged in','127.0.0.1','2026-07-23 05:42:27'),(93,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-23 16:46:31'),(94,3,'session_ended','Session 13 ended','127.0.0.1','2026-07-23 16:48:52'),(95,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-23 16:50:34'),(96,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-23 16:50:59'),(97,2,'attendance_marked','Attendance marked for session 14','127.0.0.1','2026-07-23 16:53:54'),(98,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-23 16:57:19'),(99,3,'logout','User logged out','127.0.0.1','2026-07-23 16:57:51'),(100,5,'login','User admin@example.com logged in','127.0.0.1','2026-07-23 16:57:57'),(101,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-23 17:52:32'),(102,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-23 17:52:57'),(103,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-23 17:52:58'),(104,3,'session_ended','Session 14 ended','127.0.0.1','2026-07-23 17:53:14'),(105,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-23 17:53:26'),(106,2,'attendance_marked','Attendance marked for session 15','127.0.0.1','2026-07-23 17:53:37'),(107,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-23 18:03:56'),(108,3,'session_ended','Session 15 ended','127.0.0.1','2026-07-23 18:04:07'),(109,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-23 18:04:10'),(110,3,'logout','User logged out','127.0.0.1','2026-07-23 18:04:30'),(111,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-23 18:04:37'),(112,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-23 18:06:01'),(113,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-23 18:06:01'),(114,2,'attendance_marked','Attendance marked for session 16','127.0.0.1','2026-07-23 18:06:36'),(115,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-23 18:08:21'),(116,3,'session_ended','Session 16 ended','127.0.0.1','2026-07-23 18:08:25'),(117,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-23 18:08:29'),(118,3,'session_ended','Session 17 ended','127.0.0.1','2026-07-23 18:08:35'),(119,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-28 12:19:40'),(120,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-28 12:20:01'),(121,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-28 12:20:02'),(122,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-28 12:21:16'),(123,3,'session_ended','Session 18 ended','127.0.0.1','2026-07-28 12:22:14'),(124,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-28 12:22:20'),(125,2,'attendance_marked','Attendance marked for session 19','127.0.0.1','2026-07-28 12:22:44'),(126,3,'session_ended','Session 19 ended','127.0.0.1','2026-07-28 12:30:40'),(127,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-28 12:30:58'),(128,2,'attendance_marked','Attendance marked for session 20','127.0.0.1','2026-07-28 12:31:15'),(129,3,'session_ended','Session 20 ended','127.0.0.1','2026-07-28 12:31:45'),(130,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-28 12:34:34'),(131,3,'logout','User logged out','127.0.0.1','2026-07-28 12:38:29'),(132,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-28 12:38:45'),(133,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-28 12:39:01'),(134,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-28 12:39:07'),(135,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-28 12:39:08'),(136,2,'attendance_marked','Attendance marked for session 21','127.0.0.1','2026-07-28 12:39:27'),(137,3,'session_ended','Session 21 ended','127.0.0.1','2026-07-28 12:56:29'),(138,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-28 13:00:34'),(139,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-28 13:02:25'),(140,3,'session_ended','Session 22 ended','127.0.0.1','2026-07-28 13:35:19'),(141,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-28 14:00:25'),(142,3,'logout','User logged out','127.0.0.1','2026-07-28 14:04:56'),(143,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-28 14:05:26'),(144,2,'login','User bob@example.com logged in','127.0.0.1','2026-07-28 14:07:31'),(145,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-28 14:07:44'),(146,2,'attendance_marked','Attendance marked for session 23','127.0.0.1','2026-07-28 14:08:13'),(147,46,'login','User kevin@gmail.com logged in','127.0.0.1','2026-07-28 14:28:59'),(148,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-29 20:11:23'),(149,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-29 20:11:47'),(150,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-29 20:11:47'),(151,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-29 20:11:47'),(152,3,'logout','User logged out','127.0.0.1','2026-07-29 20:36:34'),(153,3,'logout','User logged out','127.0.0.1','2026-07-29 20:36:35'),(154,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-29 21:04:13'),(155,3,'login','User sarah@example.com logged in','10.129.196.136','2026-07-29 21:10:31'),(156,3,'login','User sarah@example.com logged in','127.0.0.1','2026-07-30 05:23:45'),(157,3,'session_ended','Session 23 ended','127.0.0.1','2026-07-30 05:25:36'),(158,3,'session_started','Session started for unit 1','127.0.0.1','2026-07-30 05:25:40');
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `correction_requests`
--

DROP TABLE IF EXISTS `correction_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `correction_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `session_id` int NOT NULL,
  `reason` text NOT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `admin_comment` text,
  `submitted_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `reviewed_at` datetime DEFAULT NULL,
  PRIMARY KEY (`request_id`),
  KEY `session_id` (`session_id`),
  KEY `idx_student` (`student_id`),
  KEY `idx_status` (`status`),
  KEY `idx_submitted_at` (`submitted_at`),
  CONSTRAINT `correction_requests_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `correction_requests_ibfk_2` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`session_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `correction_requests`
--

LOCK TABLES `correction_requests` WRITE;
/*!40000 ALTER TABLE `correction_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `correction_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollments`
--

DROP TABLE IF EXISTS `enrollments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `unit_id` int NOT NULL,
  `enrolled_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`,`unit_id`),
  KEY `idx_student` (`student_id`),
  KEY `idx_unit` (`unit_id`),
  CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`unit_id`) REFERENCES `units` (`unit_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollments`
--

LOCK TABLES `enrollments` WRITE;
/*!40000 ALTER TABLE `enrollments` DISABLE KEYS */;
INSERT INTO `enrollments` VALUES (1,2,1,'2026-06-10 11:23:45');
/*!40000 ALTER TABLE `enrollments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lecturer_units`
--

DROP TABLE IF EXISTS `lecturer_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lecturer_units` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lecturer_id` int NOT NULL,
  `unit_id` int NOT NULL,
  `assigned_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lecturer_id` (`lecturer_id`,`unit_id`),
  KEY `idx_lecturer` (`lecturer_id`),
  KEY `idx_unit` (`unit_id`),
  CONSTRAINT `lecturer_units_ibfk_1` FOREIGN KEY (`lecturer_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `lecturer_units_ibfk_2` FOREIGN KEY (`unit_id`) REFERENCES `units` (`unit_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lecturer_units`
--

LOCK TABLES `lecturer_units` WRITE;
/*!40000 ALTER TABLE `lecturer_units` DISABLE KEYS */;
INSERT INTO `lecturer_units` VALUES (1,3,1,'2026-06-07 13:51:48'),(2,3,2,'2026-06-07 14:09:03'),(3,3,25,'2026-06-07 14:09:09'),(4,4,24,'2026-06-07 14:26:04');
/*!40000 ALTER TABLE `lecturer_units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `from_user_id` int DEFAULT NULL,
  `to_user_id` int DEFAULT NULL,
  `unit_id` int DEFAULT NULL,
  `message` text NOT NULL,
  `type` varchar(50) DEFAULT 'absence_warning',
  `is_read` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notification_id`),
  KEY `idx_to_user` (`to_user_id`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,3,2,1,'Dear Bob Smith, you have missed consecutive sessions. Please attend the next class or contact me. - Dr. Sarah Williams','absence_warning',1,'2026-06-11 09:32:33');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `unit_id` int NOT NULL,
  `lecturer_id` int NOT NULL,
  `session_pin` char(4) NOT NULL,
  `current_token` varchar(512) DEFAULT NULL,
  `token_generated_at` datetime DEFAULT NULL,
  `status` enum('active','closed') DEFAULT 'active',
  `start_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `end_time` datetime DEFAULT NULL,
  `session_notes` text,
  PRIMARY KEY (`session_id`),
  KEY `idx_unit` (`unit_id`),
  KEY `idx_lecturer` (`lecturer_id`),
  KEY `idx_status` (`status`),
  KEY `idx_start_time` (`start_time`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `units` (`unit_id`) ON DELETE CASCADE,
  CONSTRAINT `sessions_ibfk_2` FOREIGN KEY (`lecturer_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (1,1,3,'6655','eyJzZXNzaW9uX2lkIjogMSwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTEwVDA4OjE0OjE4LjExNTQ5OCJ9.142b41841aa8981a052cef3eda2b5db6cb4682eb046e4f856f608fb5f630f8c3','2026-06-10 08:14:18','closed','2026-06-07 14:02:11','2026-06-08 19:49:32',NULL),(2,2,3,'2536','eyJzZXNzaW9uX2lkIjogMCwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTA3VDExOjA5OjE3LjgwNzI0MyJ9.f03bd0be0b81b54ad117b77e38cca0e2c4c98570c8c0b970df209e7615f88a4a','2026-06-07 11:09:18','closed','2026-06-07 14:09:17','2026-06-08 19:49:34',NULL),(3,25,3,'8084','eyJzZXNzaW9uX2lkIjogMCwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTA3VDExOjE0OjE1LjM2OTk4OCJ9.310c7997fd45aba6af60b48aa8a38d78e576d89ed0fdf6413e5ef1ab3b04952d','2026-06-07 11:14:15','closed','2026-06-07 14:14:15','2026-06-08 19:49:36',NULL),(4,24,4,'8592','eyJzZXNzaW9uX2lkIjogMCwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTA3VDExOjI5OjAxLjMwNzgwMiJ9.43822e1978cfb532237c9372519fef2130bb57efc58a757059253cf42a229e6e','2026-06-07 11:29:01','active','2026-06-07 14:29:01',NULL,NULL),(5,1,3,'8970','eyJzZXNzaW9uX2lkIjogMCwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTA4VDE2OjQ5OjM5LjczMDE2MiJ9.090cc2cf10e0ba0b9999450d3dbdae40ad1328da308ac2be1864ad333a10a9e2','2026-06-08 16:49:40','closed','2026-06-08 19:49:39','2026-06-08 19:52:34',NULL),(6,1,3,'3921','eyJzZXNzaW9uX2lkIjogMCwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTA4VDE2OjUyOjM3LjU0MjQ0NiJ9.6b80998079334b21c77045fec654f338425b9c156ade56077b7d3bdfb5dfdd62','2026-06-08 16:52:38','closed','2026-06-08 19:52:37','2026-06-08 19:54:26',NULL),(7,1,3,'9038','eyJzZXNzaW9uX2lkIjogNywgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTA4VDE2OjU1OjQ5Ljc1OTY1NiJ9.826b8dfcaa5c6445305d9989de0e4541b6eace8b33a240d698f96978ff89c94a','2026-06-08 16:55:50','closed','2026-06-08 19:54:30','2026-06-10 10:04:18',NULL),(8,1,3,'6100','eyJzZXNzaW9uX2lkIjogMCwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTEwVDA3OjA0OjIxLjc2NzI2OSJ9.259b095974989b7d0261c92d9c75e347cdd5c5007e3b75e979225b6336f0e80d','2026-06-10 07:04:22','closed','2026-06-10 10:04:21','2026-06-10 10:54:23',NULL),(9,1,3,'8727','eyJzZXNzaW9uX2lkIjogMCwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTEwVDA4OjA3OjQ4Ljc3NjU2MiJ9.f9f5a07fc78675b4bd88f27f3c584d0cfa191309cc5ec3b65fd7a926ffb01198','2026-06-10 08:07:49','closed','2026-06-10 11:07:48','2026-06-10 11:12:41',NULL),(10,2,3,'1163','eyJzZXNzaW9uX2lkIjogMCwgInRpbWVzdGFtcCI6ICIyMDI2LTA2LTEwVDA4OjEyOjQ3LjkzNTUzOSJ9.4062e3f166c73e198e168a31ff2990d43b8bf8a5f966b9f8bddf79b1e1ff90e4','2026-06-10 08:12:48','closed','2026-06-10 11:12:47','2026-06-10 11:14:22',NULL),(11,1,3,'4072','eyJzZXNzaW9uX2lkIjogMTEsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNi0xMFQwODoxNzo0MC42NjU3MjEifQ==.44a22fa92ed0093fe01d83e7548bd52ec2779b0a7a780cfe03eacbb0577aa9f0','2026-06-10 08:17:41','closed','2026-06-10 11:14:25','2026-06-10 11:18:48',NULL),(12,1,3,'2841','eyJzZXNzaW9uX2lkIjogMTIsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNi0xN1QwMjowMDowOS4yODAwNTcifQ==.3a06341166ab301d8208babfdd0a9e666359d952a82e41c52b4e2731eb27e5ab','2026-06-17 02:00:09','closed','2026-06-17 04:59:39','2026-06-17 05:00:41',NULL),(13,1,3,'1178','eyJzZXNzaW9uX2lkIjogMTMsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNi0xN1QxODo1MzoxMy40MjQwMjEifQ==.ef9223937d20331a797188be348090b45774c7fa3e8fc36d7f95a11a9c15c6e2','2026-06-17 18:53:13','closed','2026-06-17 21:36:13','2026-07-23 16:48:52',NULL),(14,1,3,'6947','eyJzZXNzaW9uX2lkIjogMTQsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yM1QxMzo1NjozMy43MDQxMjcifQ==.98ad34f586449d3a677f7b7eaf149c867b4d1c4e0510ac5ed87eb1619e86eceb','2026-07-23 13:56:34','closed','2026-07-23 16:50:59','2026-07-23 17:53:14',NULL),(15,1,3,'1611','eyJzZXNzaW9uX2lkIjogMTUsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yM1QxNTowMzozNy4xNjc4NDEifQ==.d1dacc4483a3b47087d114467240cc52098b45d7069d07dccef3a1f45609f7c6','2026-07-23 15:03:37','closed','2026-07-23 17:53:26','2026-07-23 18:04:07',NULL),(16,1,3,'5069','eyJzZXNzaW9uX2lkIjogMTYsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yM1QxODozMTowOS4wODE2MjYifQ==.c8888d7d46b3ce2196d7b65a544456ca077ae7bd4fa1541af64ade941a902c28','2026-07-23 18:31:09','closed','2026-07-23 18:04:10','2026-07-23 18:08:25',NULL),(17,1,3,'9962','eyJzZXNzaW9uX2lkIjogMTcsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yM1QxNTowODoyOS4wNzY1MTAifQ==.ab82b4bc6adc3d0867d389e9b5f948bc444db76378fc6089e2f2dc7f38b095fc','2026-07-23 15:08:29','closed','2026-07-23 18:08:29','2026-07-23 18:08:35',NULL),(18,1,3,'0634','eyJzZXNzaW9uX2lkIjogMTgsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yOFQwOToyMTo0OS40MjkwNzEifQ==.310b522c636c5abbb4a78f657711bd08144fc390fc0d8e2c02580abb6c5cefbc','2026-07-28 09:21:49','closed','2026-07-28 12:21:16','2026-07-28 12:22:14',NULL),(19,1,3,'8101','eyJzZXNzaW9uX2lkIjogMTksICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yOFQwOTozMDozMi4xMzc1MDIifQ==.9fcbf83f796d539a502c765574760ec5dd555c6f4ec429cd3589560585d7fece','2026-07-28 09:30:32','closed','2026-07-28 12:22:20','2026-07-28 12:30:40',NULL),(20,1,3,'1096','eyJzZXNzaW9uX2lkIjogMjAsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yOFQwOTozMToyOS4yOTMwNTMifQ==.bca868911ed94cc214231f06e701df5d78bf7d523b9283211a9fecc61a4ec613','2026-07-28 09:31:29','closed','2026-07-28 12:30:58','2026-07-28 12:31:45',NULL),(21,1,3,'2768','eyJzZXNzaW9uX2lkIjogMjEsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yOFQwOTo1NjoyMS4yNTM2OTUifQ==.ae1c0f12c8bfa437963528dd63d87efb8d59c22ff3a2ebe84d687dbc9e42e597','2026-07-28 09:56:21','closed','2026-07-28 12:39:01','2026-07-28 12:56:29',NULL),(22,1,3,'8396','eyJzZXNzaW9uX2lkIjogMjIsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yOFQxMDozNTowMi4wNjE3ODAifQ==.fcebcba5feaee0a82e4bce6c4e542d22993b177244156b1919e0b80c3333e4b2','2026-07-28 10:35:02','closed','2026-07-28 13:00:33','2026-07-28 13:35:19',NULL),(23,1,3,'3294','eyJzZXNzaW9uX2lkIjogMjMsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0yOFQxNDo0MDoyMS4wMDM5ODEifQ==.77ebef18c3171a47c193f9b05a264887954141ab682336a8469fac893530312d','2026-07-28 14:40:21','closed','2026-07-28 14:07:44','2026-07-30 05:25:36',NULL),(24,1,3,'1952','eyJzZXNzaW9uX2lkIjogMjQsICJ0aW1lc3RhbXAiOiAiMjAyNi0wNy0zMFQwMjoyNjoxMS43NjIwNzkifQ==.c3a6090aa30f3cca0019e61ce68f6192493c4836e2322951db82f8149a260fd2','2026-07-30 02:26:12','active','2026-07-30 05:25:40',NULL,NULL);
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `units`
--

DROP TABLE IF EXISTS `units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `units` (
  `unit_id` int NOT NULL AUTO_INCREMENT,
  `unit_code` varchar(20) NOT NULL,
  `unit_name` varchar(150) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `semester` varchar(20) DEFAULT NULL,
  `academic_year` varchar(10) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`unit_id`),
  UNIQUE KEY `unit_code` (`unit_code`),
  KEY `idx_code` (`unit_code`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `units`
--

LOCK TABLES `units` WRITE;
/*!40000 ALTER TABLE `units` DISABLE KEYS */;
INSERT INTO `units` VALUES (1,'CS101','Introduction to Computer Science','Computer Science','1','2024','2026-06-04 06:14:35'),(2,'CS102','Data Structures','Computer Science','1','2024','2026-06-04 06:14:35'),(3,'IT101','Network Fundamentals','Information Technology','1','2024','2026-06-04 06:14:35'),(24,'cs234','intro','it','1','2','2026-06-07 12:55:55'),(25,'cs54','intro','it','2','2','2026-06-07 13:28:31');
/*!40000 ALTER TABLE `units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('student','lecturer','admin') NOT NULL,
  `registration_number` varchar(50) DEFAULT NULL,
  `staff_id` varchar(50) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Alice Johnson','alice@example.com','$2b$12$EV3EwpEvvLsJHzS/PLFEheHbppOFV/MIGsDSm8SsnVYF1JLFkHAjK','student','CS/MK/0792/09/23',NULL,NULL,0,'2026-06-04 06:14:34'),(2,'Bob Smith','bob@example.com','$2b$12$6PfKDW76mi0Y31zq8I0a2ujOs953.JIt8DanxOGVwVUbCaiEhLmHG','student','CS/MK/0793/09/23',NULL,NULL,1,'2026-06-04 06:14:34'),(3,'Dr. Sarah Williams','sarah@example.com','$2b$12$2ISUfkcWJH5ac1tYhqBJiO6tOgOhjNmecUYYb6Vd7TdUPqkDyKPmC','lecturer',NULL,'LEC001','Computer Science',1,'2026-06-04 06:14:34'),(4,'Prof. James Brown','james@example.com','$2b$12$p0pKvTHoFe28Om0AcxpQKuaHPdjumsMIheV7a7JPir7crwM5eUgEK','lecturer',NULL,'LEC002','Information Technology',1,'2026-06-04 06:14:34'),(5,'Admin User','admin@example.com','$2b$12$tMul827iVCVE1y8V/k7iz.tt2cO3/K9ZWvoXsYh2DKwQO0oe5HRQO','admin',NULL,NULL,NULL,1,'2026-06-04 06:14:35'),(6,'john','john@example.com','$2b$12$iIQPVRTBosTd6tKVLb4Lp.paIq.UIQv0u42JbBtfx5PW.HZ2ipYze','student','CS/MK/0870/09/23',NULL,NULL,1,'2026-06-04 06:21:32'),(12,'Test Student','student@test.com','$2b$12$ReUdt6dsICjpV8U8dk1UlOOolQOH7HzgJ0Nbam69iU5Vq7ZrkCMy.','student','CS/MK/0792/09/23',NULL,NULL,0,'2026-06-07 10:32:34'),(13,'Test Lecturer','lecturer@test.com','$2b$12$TYGmDGeNHL2x6gU1YK/6N.AMegQvDNZQlzQoKt4HxhnlLv1sVwjsy','lecturer',NULL,'LEC001','CS',0,'2026-06-07 10:32:34'),(34,'Unenrolled','unenrolled@test.com','$2b$12$3fejkm.UyyoU3u.hv6yyTOZ2IwOtws/iGBBFvUmQhVu4hrb6E/Dqq','student','CS/MK/0793/09/23',NULL,NULL,0,'2026-06-07 10:32:43'),(46,'Kevin','kevin@gmail.com','$2b$12$y0o7XXEpN0LfSkqOcWZz6OsvB28zDwhPvLX9AjjV6qwgD8ETx9Nju','student','CS/MK/0222/09/23',NULL,NULL,1,'2026-07-28 14:28:43');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-30  6:52:41
