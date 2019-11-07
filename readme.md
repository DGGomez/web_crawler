2. Implement a focused crawler. A focused crawler is a crawler only downloading web pages on a certain given topic. To define the initial seed set, you can start from a few known web pages on this topic. Your crawler should only crawl pages which are relevant to this topic. The relevancy could be decided by the similarity between the web page and the topic or the pages in the seed set. Since before crawling, you may not have the complete document yet, you can use the anchor text and the anchor window text (the text surrounding the anchor text). A threshold value could be defined for the relevancy judgment. You should strictly follow the Robots Exclusion Protocol during the crawling process. In your final report, you need to explain the stop criteria you use to stop the crawling process, how you follow the Robots Exclusion Protocol, how you follow the politeness policy (e.g. time gap between requests to the same site), the size of the crawled set of documents (in terms of the number of documents and the total number of bytes), and the time your program takes to complete the crawling process.

Note: Keep in mind that many HTML pages are not well-defined (not following the HTML specification strictly), your parser should be robust enough to handle this kind of pages.