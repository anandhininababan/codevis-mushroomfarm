-- phpMyAdmin SQL Dump
-- version 4.8.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 05, 2019 at 09:16 AM
-- Server version: 10.1.31-MariaDB
-- PHP Version: 7.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mushroom_farm`
--

-- --------------------------------------------------------

--
-- Table structure for table `couplingrelationship`
--

DROP TABLE IF EXISTS `couplingrelationship`;
CREATE TABLE `couplingrelationship` (
  `referenceId` int(11) NOT NULL,
  `coupledReferenceId` int(11) NOT NULL,
  `coupledReferenceName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `couplingrelationship`
--

INSERT INTO `couplingrelationship` (`referenceId`, `coupledReferenceId`, `coupledReferenceName`) VALUES
(1, 2, 'DAO'),
(4, 2, 'DAO'),
(5, 2, 'DAO'),
(5, 8, 'ProjectDAO'),
(6, 3, 'DAOMetric'),
(7, 3, 'DAOMetric'),
(8, 2, 'DAO'),
(9, 3, 'DAOMetric');

-- --------------------------------------------------------

--
-- Table structure for table `detectedmethod`
--

DROP TABLE IF EXISTS `detectedmethod`;
CREATE TABLE `detectedmethod` (
  `methodId` int(11) NOT NULL,
  `strategyId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `detectedmethod`
--

INSERT INTO `detectedmethod` (`methodId`, `strategyId`) VALUES
(1, 4),
(18, 4);

-- --------------------------------------------------------

--
-- Table structure for table `detectedpackage`
--

DROP TABLE IF EXISTS `detectedpackage`;
CREATE TABLE `detectedpackage` (
  `packageId` int(11) NOT NULL,
  `strategyId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `detectedreference`
--

DROP TABLE IF EXISTS `detectedreference`;
CREATE TABLE `detectedreference` (
  `referenceId` int(11) NOT NULL,
  `strategyId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `detectedreference`
--

INSERT INTO `detectedreference` (`referenceId`, `strategyId`) VALUES
(1, 3),
(6, 2),
(8, 5);

-- --------------------------------------------------------

--
-- Table structure for table `detectionstrategy`
--

DROP TABLE IF EXISTS `detectionstrategy`;
CREATE TABLE `detectionstrategy` (
  `strategyId` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` enum('method','reference','package') NOT NULL,
  `strategy` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `detectionstrategy`
--

INSERT INTO `detectionstrategy` (`strategyId`, `name`, `type`, `strategy`) VALUES
(1, 'Data class', 'reference', 'NSC <= threshold AND DIT <= threshold AND NOF > threshold'),
(2, 'Feature Envy', 'reference', 'LCOM >= threshold'),
(3, 'Large Class', 'reference', 'LCOM >= threshold AND WMC >= threshold AND NOF >= threshold AND NEOM >= threshold'),
(4, 'Long Method', 'method', 'MLOC >= threshold AND VG >= threshold AND NBD >= threshold'),
(5, 'Refused Bequest', 'reference', 'SIX >= threshold');

-- --------------------------------------------------------

--
-- Table structure for table `field`
--

DROP TABLE IF EXISTS `field`;
CREATE TABLE `field` (
  `fieldId` int(11) NOT NULL,
  `referenceId` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `accessModifier` enum('private','default','protected','public') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `field`
--

INSERT INTO `field` (`fieldId`, `referenceId`, `name`, `accessModifier`) VALUES
(1, 10, 'id', 'private'),
(2, 10, 'artifact', 'private'),
(3, 10, 'metric', 'private'),
(4, 10, 'subject', 'protected'),
(5, 10, 'message', 'protected'),
(6, 10, 'date', 'protected');

-- --------------------------------------------------------

--
-- Table structure for table `inheritancerelationship`
--

DROP TABLE IF EXISTS `inheritancerelationship`;
CREATE TABLE `inheritancerelationship` (
  `child` int(11) NOT NULL,
  `parent` int(11) NOT NULL,
  `parentName` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `inheritancerelationship`
--

INSERT INTO `inheritancerelationship` (`child`, `parent`, `parentName`) VALUES
(3, 2, 'DAO');

-- --------------------------------------------------------

--
-- Table structure for table `method`
--

DROP TABLE IF EXISTS `method`;
CREATE TABLE `method` (
  `methodId` int(11) NOT NULL,
  `referenceId` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `accessModifier` enum('private','default','protected','public') NOT NULL,
  `mloc` decimal(10,0) NOT NULL,
  `nbd` decimal(10,0) NOT NULL,
  `par` decimal(10,0) NOT NULL,
  `vg` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `method`
--

INSERT INTO `method` (`methodId`, `referenceId`, `name`, `accessModifier`, `mloc`, `nbd`, `par`, `vg`) VALUES
(1, 1, 'register', 'public', '9', '0', '0', '0'),
(2, 1, 'getLastID', 'private', '14', '0', '0', '0'),
(3, 1, 'register', 'public', '22', '0', '0', '0'),
(4, 1, 'registerCycleData', 'public', '34', '0', '0', '0'),
(5, 1, 'update', 'public', '55', '0', '0', '0'),
(6, 1, 'selectAll', 'public', '0', '0', '0', '0'),
(7, 1, 'selectById', 'public', '0', '0', '0', '0'),
(8, 1, 'removeCycleDataByIdProject', 'public', '0', '0', '0', '0'),
(9, 1, 'removeCycleByIdProject', 'public', '0', '0', '0', '0'),
(10, 2, 'register', 'public', '0', '0', '0', '0'),
(11, 2, 'update', 'public', '0', '0', '0', '0'),
(12, 2, 'selectAll', 'public', '0', '0', '0', '0'),
(13, 2, 'selectById', 'public', '0', '0', '0', '0'),
(14, 3, 'selectByObject', 'public', '0', '0', '0', '0'),
(15, 3, 'applyDetectionStrategy', 'public', '0', '0', '0', '0'),
(16, 3, 'totalArtifacts', 'public', '0', '0', '0', '0'),
(17, 4, 'register', 'public', '0', '0', '0', '0'),
(18, 4, 'update', 'public', '0', '0', '0', '0'),
(19, 4, 'delete', 'public', '0', '0', '0', '0'),
(20, 4, 'selectAll', 'public', '0', '0', '0', '0'),
(21, 4, 'selectById', 'public', '0', '0', '0', '0'),
(22, 4, 'selectDetectionStrategiesByFilter', 'public', '0', '0', '0', '0'),
(23, 4, 'createSqlFilter', 'private', '0', '0', '0', '0'),
(24, 4, 'remove', 'public', '0', '0', '0', '0'),
(25, 4, 'selectAllAllowed', 'public', '0', '0', '0', '0'),
(26, 5, 'register', 'public', '0', '0', '0', '0'),
(27, 5, 'update', 'public', '0', '0', '0', '0'),
(28, 5, 'selectAll', 'public', '0', '0', '0', '0'),
(29, 5, 'selectById', 'public', '0', '0', '0', '0'),
(30, 5, 'getInformationSource', 'private', '0', '0', '0', '0'),
(31, 5, 'getInformationArtifact', 'private', '0', '0', '0', '0'),
(32, 5, 'selectLogsByFilter', 'public', '0', '0', '0', '0'),
(33, 5, 'createSqlFilter', 'private', '0', '0', '0', '0'),
(34, 5, 'removeByIdProject', 'public', '0', '0', '0', '0'),
(35, 6, 'selectByObject', 'public', '0', '0', '0', '0'),
(36, 6, 'register', 'public', '0', '0', '0', '0'),
(37, 6, 'update', 'public', '0', '0', '0', '0'),
(38, 6, 'selectAll', 'public', '0', '0', '0', '0'),
(39, 6, 'selectById', 'public', '0', '0', '0', '0'),
(40, 6, 'createQuerySelectByObject', 'private', '0', '0', '0', '0'),
(41, 6, 'assignAttributeInQuery', 'private', '0', '0', '0', '0'),
(42, 6, 'applyDetectionStrategy', 'public', '0', '0', '0', '0'),
(43, 6, 'totalArtifacts', 'public', '0', '0', '0', '0'),
(44, 6, 'removeByIdProject', 'public', '0', '0', '0', '0'),
(45, 7, 'register', 'public', '0', '0', '0', '0'),
(46, 7, 'update', 'public', '0', '0', '0', '0'),
(47, 7, 'selectAll', 'public', '0', '0', '0', '0'),
(48, 7, 'selectById', 'public', '0', '0', '0', '0'),
(49, 7, 'selectByObject', 'public', '0', '0', '0', '0'),
(50, 7, 'createQuerySelectByObject', 'private', '0', '0', '0', '0'),
(51, 7, 'assignAttributeInQuery', 'private', '0', '0', '0', '0'),
(52, 7, 'applyDetectionStrategy', 'public', '0', '0', '0', '0'),
(53, 7, 'totalArtifacts', 'public', '0', '0', '0', '0'),
(54, 7, 'removeByIdProject', 'public', '0', '0', '0', '0'),
(55, 8, 'register', 'public', '0', '0', '0', '0'),
(56, 8, 'getLastID', 'public', '0', '0', '0', '0'),
(57, 8, 'register', 'public', '0', '0', '0', '0'),
(58, 8, 'selectMetricsProject', 'public', '0', '0', '0', '0'),
(59, 8, 'registerMetricProject', 'public', '0', '0', '0', '0'),
(60, 8, 'updateMetricProject', 'public', '0', '0', '0', '0'),
(61, 8, 'update', 'public', '0', '0', '0', '0'),
(62, 8, 'remove', 'public', '0', '0', '0', '0'),
(63, 8, 'removeMeasureProjectByIdProject', 'public', '0', '0', '0', '0'),
(64, 8, 'removeProject', 'private', '0', '0', '0', '0'),
(65, 8, 'selectAll', 'public', '0', '0', '0', '0'),
(66, 8, 'selectById', 'public', '0', '0', '0', '0'),
(67, 8, 'selectProjectsByFilter', 'public', '0', '0', '0', '0'),
(68, 8, 'createSqlFilter', 'private', '0', '0', '0', '0'),
(69, 9, 'selectByObject', 'public', '0', '0', '0', '0'),
(70, 9, 'register', 'public', '0', '0', '0', '0'),
(71, 9, 'update', 'public', '0', '0', '0', '0'),
(72, 9, 'selectAll', 'public', '0', '0', '0', '0'),
(73, 9, 'selectById', 'public', '0', '0', '0', '0'),
(74, 9, 'createQuerySelectByObject', 'private', '0', '0', '0', '0'),
(75, 9, 'assignAttributeInQuery', 'private', '0', '0', '0', '0'),
(76, 9, 'applyDetectionStrategy', 'public', '0', '0', '0', '0'),
(77, 9, 'totalArtifacts', 'public', '0', '0', '0', '0'),
(78, 9, 'removeByIdProject', 'public', '0', '0', '0', '0'),
(79, 10, 'writeLogCharacterInvalid', 'public', '0', '0', '0', '0'),
(80, 10, 'printLog', 'public', '0', '0', '0', '0'),
(81, 10, 'getMetric', 'public', '0', '0', '0', '0'),
(82, 10, 'getSubject', 'public', '0', '0', '0', '0'),
(83, 10, 'getArtifact', 'public', '0', '0', '0', '0'),
(84, 10, 'getMessage', 'public', '0', '0', '0', '0'),
(85, 10, 'getDate', 'public', '0', '0', '0', '0'),
(86, 10, 'getId', 'public', '0', '0', '0', '0');

-- --------------------------------------------------------

--
-- Table structure for table `methodmetricvalue`
--

DROP TABLE IF EXISTS `methodmetricvalue`;
CREATE TABLE `methodmetricvalue` (
  `methodId` int(11) NOT NULL,
  `metricId` int(11) NOT NULL,
  `value` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `metric`
--

DROP TABLE IF EXISTS `metric`;
CREATE TABLE `metric` (
  `metricId` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` enum('method','reference','package') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Table structure for table `package`
--

DROP TABLE IF EXISTS `package`;
CREATE TABLE `package` (
  `packageId` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `package`
--

INSERT INTO `package` (`packageId`, `name`) VALUES
(1, 'structure.dao'),
(2, 'structure'),
(3, 'structure.log');

-- --------------------------------------------------------

--
-- Table structure for table `packageinpackage`
--

DROP TABLE IF EXISTS `packageinpackage`;
CREATE TABLE `packageinpackage` (
  `packageId` int(11) NOT NULL,
  `container` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `packageinpackage`
--

INSERT INTO `packageinpackage` (`packageId`, `container`) VALUES
(1, 2),
(3, 2);

-- --------------------------------------------------------

--
-- Table structure for table `packagemetricvalue`
--

DROP TABLE IF EXISTS `packagemetricvalue`;
CREATE TABLE `packagemetricvalue` (
  `packageId` int(11) NOT NULL,
  `metricId` int(11) NOT NULL,
  `value` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `projectId` int(11) NOT NULL,
  `path` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `freeSmellCodePercentage` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `project`
--

INSERT INTO `project` (`projectId`, `path`, `name`, `freeSmellCodePercentage`) VALUES
(1, 'C:\\Users\\A456UQ\\workspace_anandhini\\FindSmells-master.zip', 'FindSmells-master', 88);

-- --------------------------------------------------------

--
-- Table structure for table `reference`
--

DROP TABLE IF EXISTS `reference`;
CREATE TABLE `reference` (
  `referenceId` int(11) NOT NULL,
  `packageId` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `type` enum('interface','abstract class','concrete class') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `reference`
--

INSERT INTO `reference` (`referenceId`, `packageId`, `name`, `type`) VALUES
(1, 1, 'CycleDAO', 'concrete class'),
(2, 1, 'DAO', 'interface'),
(3, 1, 'DAOMetric', 'interface'),
(4, 1, 'DetectionStrategyDAO', 'concrete class'),
(5, 1, 'LogDAO', 'concrete class'),
(6, 1, 'MethodDAO', 'concrete class'),
(7, 1, 'PackageDAO', 'concrete class'),
(8, 1, 'ProjectDAO', 'concrete class'),
(9, 1, 'TypeDAO', 'concrete class'),
(10, 3, 'Log', 'concrete class');

-- --------------------------------------------------------

--
-- Table structure for table `referencemetricvalue`
--

DROP TABLE IF EXISTS `referencemetricvalue`;
CREATE TABLE `referencemetricvalue` (
  `referenceId` int(11) NOT NULL,
  `metricId` int(11) NOT NULL,
  `value` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `visualpropertypath`
--

DROP TABLE IF EXISTS `visualpropertypath`;
CREATE TABLE `visualpropertypath` (
  `pathId` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` varchar(256) NOT NULL,
  `path` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `visualpropertypath`
--

INSERT INTO `visualpropertypath` (`pathId`, `name`, `type`, `path`) VALUES
(1, 'mushroom', 'model', 'objects/smallMushroom.obj'),
(2, 'rock', 'model', 'objects/rock.obj'),
(3, 'fence', 'model', 'objects/fence.obj'),
(4, 'RedField', 'shroom texture', 'textures/RedField.jpg'),
(5, 'RedMethod', 'shroom texture', 'textures/RedMethod.jpg'),
(6, 'YellowField', 'shroom texture', 'textures/YellowField.jpg'),
(7, 'YellowMethod', 'shroom texture', 'textures/YellowMethod.jpg'),
(8, 'BlueField', 'shroom texture', 'textures/BlueField.jpg'),
(9, 'BlueMethod', 'shroom texture', 'textures/BlueMethod.jpg'),
(10, 'GreenField', 'shroom texture', 'textures/GreenField.jpg'),
(11, 'GreenMethod', 'shroom texture', 'textures/GreenMethod.jpg'),
(12, 'score', 'gui texture', 'textures/score.jpg'),
(13, 'checkbox empty', 'gui texture', 'textures/box-s.png'),
(14, 'checkbox checked', 'gui texture', 'textures/checkedbox-s.png'),
(15, 'rock', 'texture', 'textures/rocktexture.jpg'),
(16, 'wood', 'texture', 'textures/woodtexture.jpg'),
(17, 'medMushroom', 'model', 'objects/mediumMushroom.obj'),
(18, 'larMushroom', 'model', 'objects/largeMushroom.obj');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `couplingrelationship`
--
ALTER TABLE `couplingrelationship`
  ADD KEY `referenceId` (`referenceId`),
  ADD KEY `coupledWith` (`coupledReferenceId`);

--
-- Indexes for table `detectedmethod`
--
ALTER TABLE `detectedmethod`
  ADD KEY `strategyId` (`strategyId`),
  ADD KEY `methodId` (`methodId`);

--
-- Indexes for table `detectedreference`
--
ALTER TABLE `detectedreference`
  ADD KEY `referenceId` (`referenceId`),
  ADD KEY `strategyId` (`strategyId`);

--
-- Indexes for table `detectionstrategy`
--
ALTER TABLE `detectionstrategy`
  ADD PRIMARY KEY (`strategyId`);

--
-- Indexes for table `field`
--
ALTER TABLE `field`
  ADD PRIMARY KEY (`fieldId`),
  ADD KEY `inClass` (`referenceId`);

--
-- Indexes for table `inheritancerelationship`
--
ALTER TABLE `inheritancerelationship`
  ADD KEY `ChildClass` (`child`),
  ADD KEY `ParentClass` (`parent`);

--
-- Indexes for table `method`
--
ALTER TABLE `method`
  ADD PRIMARY KEY (`methodId`),
  ADD KEY `inReference` (`referenceId`);

--
-- Indexes for table `metric`
--
ALTER TABLE `metric`
  ADD PRIMARY KEY (`metricId`);

--
-- Indexes for table `package`
--
ALTER TABLE `package`
  ADD PRIMARY KEY (`packageId`);

--
-- Indexes for table `packageinpackage`
--
ALTER TABLE `packageinpackage`
  ADD KEY `packageId` (`packageId`),
  ADD KEY `container` (`container`);

--
-- Indexes for table `packagemetricvalue`
--
ALTER TABLE `packagemetricvalue`
  ADD KEY `packagemetricvalue_ibfk_1` (`packageId`),
  ADD KEY `metricId` (`metricId`);

--
-- Indexes for table `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`projectId`);

--
-- Indexes for table `reference`
--
ALTER TABLE `reference`
  ADD PRIMARY KEY (`referenceId`),
  ADD KEY `inPackage` (`packageId`);

--
-- Indexes for table `visualpropertypath`
--
ALTER TABLE `visualpropertypath`
  ADD PRIMARY KEY (`pathId`),
  ADD KEY `path` (`path`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detectionstrategy`
--
ALTER TABLE `detectionstrategy`
  MODIFY `strategyId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `field`
--
ALTER TABLE `field`
  MODIFY `fieldId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `method`
--
ALTER TABLE `method`
  MODIFY `methodId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT for table `metric`
--
ALTER TABLE `metric`
  MODIFY `metricId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `package`
--
ALTER TABLE `package`
  MODIFY `packageId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `project`
--
ALTER TABLE `project`
  MODIFY `projectId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `reference`
--
ALTER TABLE `reference`
  MODIFY `referenceId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `visualpropertypath`
--
ALTER TABLE `visualpropertypath`
  MODIFY `pathId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `couplingrelationship`
--
ALTER TABLE `couplingrelationship`
  ADD CONSTRAINT `couplingrelationship_ibfk_1` FOREIGN KEY (`referenceId`) REFERENCES `reference` (`referenceId`),
  ADD CONSTRAINT `couplingrelationship_ibfk_2` FOREIGN KEY (`coupledReferenceId`) REFERENCES `reference` (`referenceId`);

--
-- Constraints for table `detectedmethod`
--
ALTER TABLE `detectedmethod`
  ADD CONSTRAINT `detectedmethod_ibfk_2` FOREIGN KEY (`strategyId`) REFERENCES `detectionstrategy` (`strategyId`),
  ADD CONSTRAINT `detectedmethod_ibfk_3` FOREIGN KEY (`methodId`) REFERENCES `method` (`methodId`);

--
-- Constraints for table `detectedreference`
--
ALTER TABLE `detectedreference`
  ADD CONSTRAINT `detectedreference_ibfk_1` FOREIGN KEY (`referenceId`) REFERENCES `reference` (`referenceId`),
  ADD CONSTRAINT `detectedreference_ibfk_2` FOREIGN KEY (`strategyId`) REFERENCES `detectionstrategy` (`strategyId`);

--
-- Constraints for table `field`
--
ALTER TABLE `field`
  ADD CONSTRAINT `field_ibfk_1` FOREIGN KEY (`referenceId`) REFERENCES `reference` (`referenceId`);

--
-- Constraints for table `inheritancerelationship`
--
ALTER TABLE `inheritancerelationship`
  ADD CONSTRAINT `inheritancerelationship_ibfk_1` FOREIGN KEY (`child`) REFERENCES `reference` (`referenceId`),
  ADD CONSTRAINT `inheritancerelationship_ibfk_2` FOREIGN KEY (`parent`) REFERENCES `reference` (`referenceId`);

--
-- Constraints for table `method`
--
ALTER TABLE `method`
  ADD CONSTRAINT `method_ibfk_1` FOREIGN KEY (`referenceId`) REFERENCES `reference` (`referenceId`);

--
-- Constraints for table `packageinpackage`
--
ALTER TABLE `packageinpackage`
  ADD CONSTRAINT `packageinpackage_ibfk_1` FOREIGN KEY (`packageId`) REFERENCES `package` (`packageId`),
  ADD CONSTRAINT `packageinpackage_ibfk_2` FOREIGN KEY (`container`) REFERENCES `package` (`packageId`);

--
-- Constraints for table `packagemetricvalue`
--
ALTER TABLE `packagemetricvalue`
  ADD CONSTRAINT `packagemetricvalue_ibfk_1` FOREIGN KEY (`packageId`) REFERENCES `package` (`packageId`),
  ADD CONSTRAINT `packagemetricvalue_ibfk_2` FOREIGN KEY (`metricId`) REFERENCES `metric` (`metricId`);

--
-- Constraints for table `reference`
--
ALTER TABLE `reference`
  ADD CONSTRAINT `reference_ibfk_1` FOREIGN KEY (`packageId`) REFERENCES `package` (`packageId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
