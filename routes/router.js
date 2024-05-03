// router.js
const express = require("express");
const router = express.Router();
const puppeteer = require("puppeteer");
const Product = require("../models/Product");
const scrapeData = require("../utils/scrapeData");

router.get("/scrape", (req, res) => {
  res.render("scrape");
});

router.get("/searchProduct", (req, res) => {
  res.render("searchProduct");
});

router.get("/scrapeResults", async function (req, res) {
  let url = req.query.search;

  let browser;

  try {
    browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    let data = await scrapeData(url, page);

    // Check if a product with the same title already exists in the database
    const existingProduct = await Product.findOne({ title: data.title });

    if (existingProduct) {
      console.log("Product with the same title already exists, skipping save.");
      res.render("scrapeResults", { product: existingProduct });
    } else {
      // Save the scraped product into the database
      const product = new Product({
        title: data.title,
        price: data.price,
        discount: data.discount,
        productDetails: data.productDetails,
        imgUrl: data.imgUrl,
      });

      console.log(product);

      await product.save();

      res.render("scrapeResults", { product: product });
    }
  } catch (error) {
    console.log(error);
    res.status(500).send("Error scraping data");
  } finally {
    if (browser) {
      await browser.close();
    }
  }
});

router.get("/resultsproducts", async (req, res) => {
  try {
    const searchTitle = req.query.title;

    // Search for products with exact title match in the database
    const products = await Product.find({ title: searchTitle });

    res.render("resultsproducts", { products: products });
  } catch (error) {
    console.log(error);
    res.status(500).send("Error searching products");
  }
});

module.exports = router;
