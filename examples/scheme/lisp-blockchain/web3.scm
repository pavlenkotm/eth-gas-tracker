#!/usr/bin/env guile
!#

;;; Scheme Web3 Client - Lisp-powered blockchain interactions

(use-modules (web client)
             (web response)
             (json)
             (ice-9 format)
             (ice-9 receive))

(define rpc-url "https://eth.llamarpc.com")
(define request-id 0)

(define (rpc-call method params)
  "Make JSON-RPC call to Ethereum node"
  (set! request-id (+ request-id 1))

  (let* ((payload (scm->json-string
                   `(("jsonrpc" . "2.0")
                     ("method" . ,method)
                     ("params" . ,params)
                     ("id" . ,request-id))))
         (response (http-post rpc-url
                             #:body payload
                             #:headers '((content-type . (application/json)))))
         (body (json-string->scm (receive (resp body) response
                                   (utf8->string body)))))
    (assoc-ref body "result")))

(define (hex->int hex)
  "Convert hex string to integer"
  (string->number (substring hex 2) 16))

(define (wei->ether wei)
  "Convert wei to ether"
  (/ wei 1e18))

(define (wei->gwei wei)
  "Convert wei to gwei"
  (/ wei 1e9))

(define (get-block-number)
  "Get latest block number"
  (hex->int (rpc-call "eth_blockNumber" '())))

(define (get-balance address)
  "Get balance of address in ETH"
  (wei->ether
    (hex->int
      (rpc-call "eth_getBalance" `(,address "latest")))))

(define (get-gas-price)
  "Get current gas price in Gwei"
  (wei->gwei
    (hex->int
      (rpc-call "eth_gasPrice" '()))))

;; Example usage
(when (batch-mode?)
  (format #t "🎨 Scheme Web3 Client~%")
  (format #t "~a~%" (make-string 40 #\-))

  (let ((block (get-block-number))
        (gas (get-gas-price))
        (address "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"))

    (format #t "📦 Block Number: ~a~%" block)
    (format #t "⛽ Gas Price: ~,2f Gwei~%" gas)
    (format #t "💰 Balance: ~,4f ETH~%" (get-balance address))))
