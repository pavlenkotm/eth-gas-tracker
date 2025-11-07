const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SimpleToken", function () {
  let simpleToken;
  let owner;
  let addr1;
  let addr2;

  beforeEach(async function () {
    [owner, addr1, addr2] = await ethers.getSigners();

    const SimpleToken = await ethers.getContractFactory("SimpleToken");
    simpleToken = await SimpleToken.deploy(
      "Simple Token",
      "SMPL",
      18,
      1000000, // 1M initial supply
      10000000 // 10M max supply
    );
    await simpleToken.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await simpleToken.owner()).to.equal(owner.address);
    });

    it("Should assign the initial supply to the owner", async function () {
      const ownerBalance = await simpleToken.balanceOf(owner.address);
      expect(await simpleToken.totalSupply()).to.equal(ownerBalance);
    });

    it("Should have correct decimals", async function () {
      expect(await simpleToken.decimals()).to.equal(18);
    });
  });

  describe("Minting", function () {
    it("Should mint tokens to specified address", async function () {
      const mintAmount = ethers.parseUnits("1000", 18);
      await simpleToken.mint(addr1.address, mintAmount);
      expect(await simpleToken.balanceOf(addr1.address)).to.equal(mintAmount);
    });

    it("Should fail if non-owner tries to mint", async function () {
      const mintAmount = ethers.parseUnits("1000", 18);
      await expect(
        simpleToken.connect(addr1).mint(addr2.address, mintAmount)
      ).to.be.reverted;
    });

    it("Should not exceed max supply", async function () {
      const maxSupply = await simpleToken.maxSupply();
      const currentSupply = await simpleToken.totalSupply();
      const excessAmount = maxSupply - currentSupply + 1n;

      await expect(
        simpleToken.mint(addr1.address, excessAmount)
      ).to.be.revertedWith("Minting would exceed max supply");
    });
  });

  describe("Burning", function () {
    it("Should burn tokens from caller", async function () {
      const burnAmount = ethers.parseUnits("1000", 18);
      const initialBalance = await simpleToken.balanceOf(owner.address);

      await simpleToken.burn(burnAmount);

      const finalBalance = await simpleToken.balanceOf(owner.address);
      expect(finalBalance).to.equal(initialBalance - burnAmount);
    });

    it("Should fail to burn more than balance", async function () {
      const balance = await simpleToken.balanceOf(owner.address);
      await expect(simpleToken.burn(balance + 1n)).to.be.reverted;
    });
  });

  describe("Transfers", function () {
    it("Should transfer tokens between accounts", async function () {
      const transferAmount = ethers.parseUnits("100", 18);

      await simpleToken.transfer(addr1.address, transferAmount);
      expect(await simpleToken.balanceOf(addr1.address)).to.equal(transferAmount);

      await simpleToken.connect(addr1).transfer(addr2.address, transferAmount);
      expect(await simpleToken.balanceOf(addr2.address)).to.equal(transferAmount);
    });

    it("Should fail if sender doesn't have enough tokens", async function () {
      const initialOwnerBalance = await simpleToken.balanceOf(owner.address);
      await expect(
        simpleToken.connect(addr1).transfer(owner.address, 1)
      ).to.be.reverted;

      expect(await simpleToken.balanceOf(owner.address)).to.equal(
        initialOwnerBalance
      );
    });
  });
});
