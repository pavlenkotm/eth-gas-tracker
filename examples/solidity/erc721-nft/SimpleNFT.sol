// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title SimpleNFT
 * @dev ERC-721 NFT contract with minting, metadata, and royalty support
 * @notice Example implementation showcasing OpenZeppelin best practices
 */
contract SimpleNFT is ERC721, ERC721URIStorage, ERC721Burnable, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;
    uint256 public maxSupply;
    uint256 public mintPrice;
    string public baseTokenURI;
    bool public publicMintEnabled;

    // Royalty info (EIP-2981 compatible)
    address public royaltyReceiver;
    uint96 public royaltyFeeNumerator; // Basis points (e.g., 250 = 2.5%)

    event NFTMinted(address indexed to, uint256 indexed tokenId, string tokenURI);
    event PublicMintToggled(bool enabled);
    event MintPriceUpdated(uint256 newPrice);
    event BaseURIUpdated(string newBaseURI);
    event RoyaltyUpdated(address receiver, uint96 feeNumerator);

    /**
     * @dev Constructor to initialize the NFT collection
     * @param name_ Collection name
     * @param symbol_ Collection symbol
     * @param baseURI_ Base URI for token metadata
     * @param maxSupply_ Maximum number of NFTs (0 for unlimited)
     * @param mintPrice_ Price per mint in wei
     */
    constructor(
        string memory name_,
        string memory symbol_,
        string memory baseURI_,
        uint256 maxSupply_,
        uint256 mintPrice_
    ) ERC721(name_, symbol_) Ownable(msg.sender) {
        baseTokenURI = baseURI_;
        maxSupply = maxSupply_;
        mintPrice = mintPrice_;
        publicMintEnabled = false;
        royaltyReceiver = msg.sender;
        royaltyFeeNumerator = 250; // 2.5% default royalty
    }

    /**
     * @dev Base URI for computing tokenURI
     */
    function _baseURI() internal view override returns (string memory) {
        return baseTokenURI;
    }

    /**
     * @dev Mint NFT (owner only)
     * @param to Address to receive the NFT
     * @param uri Token metadata URI
     */
    function safeMint(address to, string memory uri) public onlyOwner {
        uint256 tokenId = _tokenIdCounter.current();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        _tokenIdCounter.increment();

        emit NFTMinted(to, tokenId, uri);
    }

    /**
     * @dev Public mint function
     * @param uri Token metadata URI
     */
    function publicMint(string memory uri) public payable {
        require(publicMintEnabled, "Public minting is not enabled");
        require(msg.value >= mintPrice, "Insufficient payment");

        if (maxSupply > 0) {
            require(_tokenIdCounter.current() < maxSupply, "Max supply reached");
        }

        uint256 tokenId = _tokenIdCounter.current();
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);
        _tokenIdCounter.increment();

        emit NFTMinted(msg.sender, tokenId, uri);

        // Refund excess payment
        if (msg.value > mintPrice) {
            payable(msg.sender).transfer(msg.value - mintPrice);
        }
    }

    /**
     * @dev Batch mint multiple NFTs (owner only)
     * @param to Address to receive the NFTs
     * @param uris Array of token metadata URIs
     */
    function batchMint(address to, string[] memory uris) public onlyOwner {
        require(uris.length > 0, "Must mint at least one NFT");

        if (maxSupply > 0) {
            require(
                _tokenIdCounter.current() + uris.length <= maxSupply,
                "Batch mint would exceed max supply"
            );
        }

        for (uint256 i = 0; i < uris.length; i++) {
            uint256 tokenId = _tokenIdCounter.current();
            _safeMint(to, tokenId);
            _setTokenURI(tokenId, uris[i]);
            _tokenIdCounter.increment();

            emit NFTMinted(to, tokenId, uris[i]);
        }
    }

    /**
     * @dev Toggle public minting
     * @param enabled Enable or disable public minting
     */
    function setPublicMintEnabled(bool enabled) public onlyOwner {
        publicMintEnabled = enabled;
        emit PublicMintToggled(enabled);
    }

    /**
     * @dev Update mint price
     * @param newPrice New mint price in wei
     */
    function setMintPrice(uint256 newPrice) public onlyOwner {
        mintPrice = newPrice;
        emit MintPriceUpdated(newPrice);
    }

    /**
     * @dev Update base URI
     * @param newBaseURI New base URI
     */
    function setBaseURI(string memory newBaseURI) public onlyOwner {
        baseTokenURI = newBaseURI;
        emit BaseURIUpdated(newBaseURI);
    }

    /**
     * @dev Set royalty info (EIP-2981)
     * @param receiver Address to receive royalties
     * @param feeNumerator Royalty fee in basis points (e.g., 250 = 2.5%)
     */
    function setRoyaltyInfo(address receiver, uint96 feeNumerator) public onlyOwner {
        require(feeNumerator <= 10000, "Royalty fee too high");
        royaltyReceiver = receiver;
        royaltyFeeNumerator = feeNumerator;
        emit RoyaltyUpdated(receiver, feeNumerator);
    }

    /**
     * @dev Get royalty info for a token sale (EIP-2981)
     * @param salePrice Sale price of the NFT
     */
    function royaltyInfo(uint256, uint256 salePrice)
        public
        view
        returns (address receiver, uint256 royaltyAmount)
    {
        receiver = royaltyReceiver;
        royaltyAmount = (salePrice * royaltyFeeNumerator) / 10000;
    }

    /**
     * @dev Withdraw contract balance (owner only)
     */
    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to withdraw");
        payable(owner()).transfer(balance);
    }

    /**
     * @dev Get total supply minted
     */
    function totalSupply() public view returns (uint256) {
        return _tokenIdCounter.current();
    }

    // Required overrides
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
