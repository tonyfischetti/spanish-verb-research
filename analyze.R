#!/usr/bin/Rscript --vanilla

###########################################################
##                                                       ##
##   analyze.R                                           ##
##                                                       ##
##                Author: Tony Fischetti                 ##
##                        tony.fischetti@gmail.com       ##
##                                                       ##
###########################################################

# workspace cleanup
rm(list=ls())


# options
options(echo=TRUE)
options(stringsAsFactors=FALSE)

# cli args
args <- commandArgs(trailingOnly=TRUE)

# libraries
library(data.table)
library(dplyr)
library(magrittr)
library(assertr)
library(tidyr)
library(ggplot2)
library(wesanderson)
library(RColorBrewer)
library(ggthemes)

verbs <- fread("./tagged-plus-infinitives.txt")

NUM.VERBS <- nrow(verbs)

most.common.conjugated.verbs <- verbs %>%
  group_by(conjugated_verb) %>%
  summarise(count=n()) %>%
  arrange(desc(count)) %>%
  mutate(perc = (count/NUM.VERBS)*100)
most.common.conjugated.verbs %>% write.csv("most-common-conjugated-verbs.csv",
                                           row.names=FALSE)


most.common.infinitives <- verbs %>%
  group_by(infinitive) %>%
  summarise(count=n()) %>%
  arrange(desc(count)) %>%
  mutate(perc = (count/NUM.VERBS)*100)
most.common.infinitives %>% write.csv("most-common-infinitives.csv",
                                      row.names=FALSE)


most.common.moods <- verbs %>%
  group_by(mood) %>%
  summarise(count=n()) %>%
  arrange(desc(count)) %>%
  mutate(perc = (count/NUM.VERBS)*100)
most.common.moods %>% write.csv("most-common-moods.csv",
                                row.names=FALSE)


most.common.moods.and.tenses <- verbs %>%
  group_by(mood, tense) %>%
  summarise(count=n()) %>%
  arrange(desc(count)) %>%
  mutate(perc = (count/NUM.VERBS)*100)
most.common.moods.and.tenses %>% write.csv("most-common-moods-and-tenses.csv",
                                           row.names=FALSE)


df <- most.common.moods.and.tenses %>%
  filter(tense!="conditional")   # too few observations
this <- df %>% group_by(mood) %>% summarise(mperc=sum(perc))
df %<>% left_join(this) %>% arrange(desc(mperc), desc(perc))

df$lab <- ifelse(df$perc>.8, df$tense, "")
df$lab3 <- c("present", "imperfect", "preterite", "future", "", "",
             "imperfect", "present", "", "", "", "")
df$lab2 <- ifelse(df$lab!="", paste0(df$lab, " \n(perc)"), "")
neww <- c(12.885, 36.22, 55.3, 64.5, 66, 9.765, 2.13, 6.03, 0, 5.5, 4.5, 2.3)
df$neww <- neww

positions <- c("indicative", "infinitive",
               "subjunctive", "participle",
               "gerund", "imperative")
cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442",
               "#0072B2", "#D55E00", "#CC79A7", "#000000")
otherPalette <- c("#8dd3c7", "#ffffb3", "#bebada",
                  "#fb8072", "#80b1d3", "#fdb462",
                  "#b3de69", "#fccde5")#, "#d9d9d9")


ggplot(df,
       aes(y=perc, x=mood,
           fill=tense,
           label=lab3)) +
  geom_bar(stat="identity") +
  geom_text(aes(y=neww)) +
  scale_x_discrete(limits = positions) +
  ylab("percentage") +
  ggtitle("Proportion Spanish verb\nmoods and tenses in corpus") +
  #theme_stata() + scale_color_stata() +
  theme_wsj() + scale_colour_wsj() +    # i like this one
  #theme_solarized(light = FALSE) + scale_colour_solarized("red") +
  #theme_pander() + scale_fill_pander() +
  #theme_fivethirtyeight() +
  #scale_fill_manual(values=cbPalette) +
  #scale_fill_brewer(palette="Set3") +
  scale_fill_manual(values=otherPalette) +
  theme(legend.position="none") + ggsave("plot.png")
########################################################
