SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


CREATE DATABASE IF NOT EXISTS `mark5463_ft_prod` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `mark5463_ft_prod`;

-- --------------------------------------------------------

--
-- Table structure for table `mma_org`
--

CREATE TABLE `mma_org` (
  `mma_org` varchar(20) NOT NULL,
  `sd_event_id` int(11) NOT NULL,
  `wiki_event_id` int(11) NOT NULL,
  `sd_event_name` int(11) NOT NULL,
  `wiki_event_name` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sd_mma_events`
--

CREATE TABLE `sd_mma_events` (
  `event_day` int(11) NOT NULL,
  `event_fight_card_url` varchar(350) NOT NULL,
  `event_id` int(11) NOT NULL,
  `event_location` varchar(200) NOT NULL,
  `event_month` char(3) NOT NULL,
  `event_name` varchar(75) NOT NULL,
  `event_org` varchar(30) NOT NULL,
  `event_year` int(11) NOT NULL,
  `sd_event_id` varchar(100) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sd_mma_fight_cards`
--

CREATE TABLE `sd_mma_fight_cards` (
  `event_name` varchar(150) NOT NULL,
  `fighter_one` varchar(150) NOT NULL,
  `fighter_one_url` varchar(150) NOT NULL,
  `fighter_two` varchar(150) NOT NULL,
  `fighter_two_url` varchar(150) NOT NULL,
  `event_url` varchar(300) NOT NULL,
  `event_org` varchar(20) NOT NULL,
  `event_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_mma_events`
--

CREATE TABLE `wiki_mma_events` (
  `event_name` varchar(250) NOT NULL,
  `event_id` int(11) NOT NULL,
  `event_fight_card_url` varchar(300) NOT NULL,
  `event_org` varchar(200) NOT NULL,
  `event_date` varchar(50) NOT NULL,
  `wiki_event_id` varchar(100) NOT NULL,
  `event_past` boolean NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_mma_events_poster`
--

CREATE TABLE `wiki_mma_events_poster` (
  `event_fight_poster_url` varchar(500) NOT NULL,
  `event_id` int(11) NOT NULL,
  `event_fight_card_url` varchar(250) NOT NULL,
  `event_name` varchar(300) NOT NULL,
  `event_date` varchar(50) NOT NULL,
  `event_org` varchar(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `wiki_mma_fight_cards`
--

CREATE TABLE `wiki_mma_fight_cards` (
  `event_name` varchar(500) NOT NULL,
  `event_url` varchar(500) NOT NULL,
  `fighter_one` varchar(500) NOT NULL,
  `fighter_one_url` varchar(500) NOT NULL,
  `fighter_two` varchar(500) NOT NULL,
  `fighter_two_url` varchar(500) NOT NULL,
  `event_org` varchar(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
COMMIT;

