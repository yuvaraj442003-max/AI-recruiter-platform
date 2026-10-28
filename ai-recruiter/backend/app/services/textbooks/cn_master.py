"""
cn_master.py — Prescribed Master Textbook for Computer Networks (CN).
Comprehensive unabridged campus placement textbook covering OSI 7-layer model,
TCP/IP architecture, framing & CRC error detection, sliding window flow control,
IPv4/IPv6, CIDR subnetting math, routing algorithms (Dijkstra, Bellman-Ford),
TCP reliability & congestion control, HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC), DNS,
TLS 1.3 cryptographic handshake, solved numericals, and placement interview questions.
"""

CN_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "OSI 7-Layer Reference Model vs TCP/IP Protocol Architecture",
        "topics": [
            "Physical, Data Link, Network, Transport, Session, Presentation, Application layers",
            "Protocol Data Units (PDUs): Bits, Frames, Packets, Segments, Messages",
            "Encapsulation and decapsulation headers across network interfaces",
            "Hardware (MAC) vs Logical (IP) vs Port (Process) addressing hierarchy",
            "Network devices: Hubs (L1), Switches & Bridges (L2), Routers & Gateways (L3)"
        ],
        "key_takeaways": "Each layer provides services to the layer above and consumes services from the layer below. Routers operate at Layer 3 (Network); Switches operate at Layer 2 (Data Link)."
    },
    {
        "chapter_num": 2,
        "title": "Data Link Layer, Framing & Error Control Protocols",
        "topics": [
            "Framing techniques: Character count, Byte stuffing, and Bit stuffing (flag 01111110)",
            "Error detection algorithms: Parity check, Checksum, and Cyclic Redundancy Check (CRC-32)",
            "Flow control mechanisms: Stop-and-Wait, Go-Back-N (GBN), and Selective Repeat (SR)",
            "Medium Access Control (MAC): CSMA/CD (Ethernet collision detection) and CSMA/CA (Wi-Fi)",
            "Minimum frame size theorem in CSMA/CD: L >= 2 * Propagation Time * Bandwidth"
        ],
        "key_takeaways": "CRC uses polynomial long division over Galois Field GF(2). In Go-Back-N, receiver window is 1; in Selective Repeat, sender and receiver windows are both 2^(m-1), retransmitting only erroneous frames."
    },
    {
        "chapter_num": 3,
        "title": "Network Layer: IPv4, IPv6, Subnetting & Routing Protocols",
        "topics": [
            "IPv4 header structure (TTL, Flags, Fragmentation fields) and IPv6 improvements",
            "Classless Inter-Domain Routing (CIDR) subnet mask calculations and VLSM partitioning",
            "Address Resolution Protocol (ARP) and Network Address Translation (NAT / PAT)",
            "Distance Vector Routing (Bellman-Ford, Count-to-Infinity problem & Split Horizon)",
            "Link State Routing (Dijkstra's Shortest Path First, OSPF, Link State Advertisements)"
        ],
        "key_takeaways": "Subnet mask /26 divides a network into 4 subnets with 64 IP addresses each (62 usable host addresses). TTL prevents packets from circulating indefinitely in routing loops."
    },
    {
        "chapter_num": 4,
        "title": "Transport Layer: TCP Reliability, Flow & Congestion Control",
        "topics": [
            "TCP (connection-oriented, reliable, byte-stream) vs UDP (connectionless, datagram)",
            "TCP 3-Way Handshake (SYN -> SYN-ACK -> ACK) and 4-Way Connection Teardown (FIN -> ACK)",
            "TIME_WAIT state rationale (2 * MSL) to ensure duplicate packets dissipate",
            "Flow control via Sliding Window and Nagle's algorithm (Silly Window syndrome)",
            "Congestion Control state machine: Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery"
        ],
        "key_takeaways": "Flow control prevents sender from overwhelming receiver (via Receiver Window rwnd); Congestion control prevents sender from overwhelming network intermediate routers (via Congestion Window cwnd)."
    },
    {
        "chapter_num": 5,
        "title": "Application Layer Protocols: HTTP, DNS, TLS & WebSockets",
        "topics": [
            "Evolution of web protocols: HTTP/1.1 (pipelining, head-of-line blocking) vs HTTP/2 (multiplexing) vs HTTP/3 (QUIC / UDP)",
            "Domain Name System (DNS) recursive vs iterative query resolution flow",
            "Transport Layer Security (TLS 1.3) cryptographic handshake and certificate verification",
            "WebSockets full-duplex persistent bidirectional communication vs HTTP polling",
            "Email protocols: SMTP (push, port 25/587) vs IMAP/POP3 (pull, port 993/995)"
        ],
        "key_takeaways": "HTTP/2 introduces binary framing and stream multiplexing over a single TCP connection, but suffers from TCP-level head-of-line blocking. HTTP/3 resolves this by running over QUIC (UDP)."
    },
    {
        "chapter_num": 6,
        "title": "Solved Networking Placement Numericals & Interview Drills",
        "topics": [
            "Subnetting & VLSM IP allocation numericals",
            "CRC error detection generator polynomial step-by-step division",
            "Sliding window protocol efficiency & throughput calculations",
            "CSMA/CD minimum frame length determination for high-speed Ethernet",
            "TCP sequence number arithmetic and congestion window tracing"
        ],
        "key_takeaways": "Mastering subnet mask conversion, CRC bit-shifting, and TCP sequence/ACK number tracing guarantees high scores in technical tests for Cisco, Amazon, Google, and TCS Digital."
    }
]

CN_TEXTBOOK_MARKDOWN = r"""# Computer Networks & Internet Protocols: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Computer Networks (CN)  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, network engineering technical interviews, and online test questions are strictly grounded in the protocols, layer models, subnetting formulas, and RFC standards detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: OSI 7-Layer Reference Model vs TCP/IP Protocol Architecture](#chapter-1-osi-7-layer-reference-model-vs-tcpip-protocol-architecture)
  - [1.1 The Theoretical OSI 7-Layer Architecture](#11-the-theoretical-osi-7-layer-architecture)
  - [1.2 Protocol Data Units (PDUs) & Encapsulation Stack](#12-protocol-data-units-pdus--encapsulation-stack)
  - [1.3 Hardware Devices by Layer: Hubs, Switches, Routers & Gateways](#13-hardware-devices-by-layer-hubs-switches-routers--gateways)
  - [1.4 The 4-Layer TCP/IP Real-World Model](#14-the-4-layer-tcpip-real-world-model)
- [Chapter 2: Data Link Layer, Framing & Error Control Protocols](#chapter-2-data-link-layer-framing--error-control-protocols)
  - [2.1 Framing Mechanics: Byte Stuffing & Bit Stuffing](#21-framing-mechanics-byte-stuffing--bit-stuffing)
  - [2.2 Error Detection: Parity, Checksum & CRC Polynomial Math](#22-error-detection-parity-checksum--crc-polynomial-math)
  - [2.3 Flow Control: Stop-and-Wait, Go-Back-N & Selective Repeat](#23-flow-control-stop-and-wait-go-back-n--selective-repeat)
  - [2.4 Medium Access Control: CSMA/CD & CSMA/CA](#24-medium-access-control-csmacd--csmaca)
- [Chapter 3: Network Layer: IPv4, IPv6, Subnetting & Routing Protocols](#chapter-3-network-layer-ipv4-ipv6-subnetting--routing-protocols)
  - [3.1 IPv4 Header Architecture & Packet Fragmentation](#31-ipv4-header-architecture--packet-fragmentation)
  - [3.2 CIDR Subnetting Math & VLSM Design](#32-cidr-subnetting-math--vlsm-design)
  - [3.3 Address Resolution Protocol (ARP) & NAT/PAT](#33-address-resolution-protocol-arp--natpat)
  - [3.4 Routing Protocols: Distance Vector vs Link State Routing](#34-routing-protocols-distance-vector-vs-link-state-routing)
- [Chapter 4: Transport Layer: TCP Reliability, Flow & Congestion Control](#chapter-4-transport-layer-tcp-reliability-flow--congestion-control)
  - [4.1 TCP vs UDP Architectural Comparison](#41-tcp-vs-udp-architectural-comparison)
  - [4.2 TCP 3-Way Handshake & 4-Way Teardown (TIME_WAIT Deep Dive)](#42-tcp-3-way-handshake--4-way-teardown-timewait-deep-dive)
  - [4.3 Sliding Window Flow Control & Silly Window Prevention](#43-sliding-window-flow-control--silly-window-prevention)
  - [4.4 TCP Congestion Control State Machine](#44-tcp-congestion-control-state-machine)
- [Chapter 5: Application Layer Protocols: HTTP, DNS, TLS & WebSockets](#chapter-5-application-layer-protocols-http-dns-tls--websockets)
  - [5.1 The Evolution of Web Protocols: HTTP/1.1 vs HTTP/2 vs HTTP/3](#51-the-evolution-of-web-protocols-http11-vs-http2-vs-http3)
  - [5.2 Domain Name System (DNS) Architecture](#52-domain-name-system-dns-architecture)
  - [5.3 Transport Layer Security (TLS 1.3) Cryptographic Handshake](#53-transport-layer-security-tls-13-cryptographic-handshake)
  - [5.4 WebSockets Full-Duplex Real-Time Communication](#54-websockets-full-duplex-real-time-communication)
- [Chapter 6: Solved Networking Placement Numericals & Interview Drills](#chapter-6-solved-networking-placement-numericals--interview-drills)
  - [Solved Problem 1: CIDR VLSM Subnet Allocation](#solved-problem-1-cidr-vlsm-subnet-allocation)
  - [Solved Problem 2: CRC-32 Frame Generation & Check](#solved-problem-2-crc-32-frame-generation--check)
  - [Solved Problem 3: CSMA/CD Minimum Packet Size Determination](#solved-problem-3-csmacd-minimum-packet-size-determination)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: OSI 7-Layer Reference Model vs TCP/IP Protocol Architecture

### 1.1 The Theoretical OSI 7-Layer Architecture
The Open Systems Interconnection (OSI) model was developed by the International Organization for Standardization (ISO) in 1984 as an architectural blueprint for open communication between disparate computer systems. The 7 layers, numbered bottom-up from Layer 1 to Layer 7:

```
[ Layer 7: Application  ] -> End-user applications, APIs (HTTP, DNS, SSH, FTP, SMTP)
[ Layer 6: Presentation ] -> Syntax, data formatting, encryption (TLS), compression (JPEG)
[ Layer 5: Session      ] -> Dialog management, token management, session sync (Sockets, RPC)
[ Layer 4: Transport    ] -> End-to-end reliability, segmentation, port addressing (TCP, UDP)
[ Layer 3: Network      ] -> Logical routing, logical addressing, path selection (IPv4, IPv6, ICMP)
[ Layer 2: Data Link    ] -> Physical addressing (MAC), framing, hop-to-hop flow/error control
[ Layer 1: Physical     ] -> Bitstream transmission over physical media (Cables, Fiber, RF)
```

### 1.2 Protocol Data Units (PDUs) & Encapsulation Stack
As application data travels down the protocol stack on the sending host, each layer prepends a header containing metadata (and occasionally appends a trailer), a process known as **Encapsulation**:

1. **Application Data:** Raw message generated by the user application (e.g., `GET /index.html HTTP/1.1`).
2. **Transport Layer PDU:** Adds a TCP or UDP header containing Source Port (16-bit) and Destination Port (16-bit). The PDU is termed a **Segment** (TCP) or **Datagram** (UDP).
3. **Network Layer PDU:** Adds an IP header containing Source IP (32-bit for IPv4) and Destination IP (32-bit). The PDU is termed a **Packet**.
4. **Data Link Layer PDU:** Adds a MAC header containing Source MAC (48-bit) and Destination MAC (48-bit), plus an FCS (Frame Check Sequence) trailer. The PDU is termed a **Frame**.
5. **Physical Layer PDU:** The frame is encoded into electromagnetic or optical signals as raw **Bits**.

On the receiving host, the process is reversed (**Decapsulation**): each layer strips its corresponding header, verifies checksums, and dispatches the payload to the appropriate entity in the layer above.

### 1.3 Hardware Devices by Layer: Hubs, Switches, Routers & Gateways
| Device | Operating OSI Layer | Addressing Scheme | Collision Domain | Broadcast Domain | Functionality |
|:---|:---|:---|:---|:---|:---|
| **Hub / Repeater** | Layer 1 (Physical) | None (Blind Electrical) | 1 Shared Collision Domain | 1 Shared Broadcast Domain | Amplifies and broadcasts electrical signals to all connected physical ports. |
| **Bridge / Switch** | Layer 2 (Data Link) | 48-bit MAC Addresses | Separate Collision Domain per port | 1 Shared Broadcast Domain | Maintains a CAM (Content Addressable Memory) MAC address table to forward frames selectively. |
| **Router** | Layer 3 (Network) | 32-bit IPv4 / 128-bit IPv6 | Separate Collision Domain per port | Separate Broadcast Domain per interface | Evaluates routing tables to forward packets across subnet boundaries. |
| **Gateway / Proxy** | Layer 4-7 (Application) | IP + Port + Protocol payload | Isolated | Isolated | Performs application-layer protocol translation, load balancing, or deep packet inspection. |

---

## Chapter 2: Data Link Layer, Framing & Error Control Protocols

### 2.1 Framing Mechanics: Byte Stuffing & Bit Stuffing
To allow the receiver to recognize frame boundaries, the sender encapsulates frames between delimiter patterns:

- **Byte Stuffing (Character-Oriented Framing):**
  Uses special control bytes `FLAG` (e.g., `0x7E`) and `ESC` (Escape, e.g., `0x7D`). Whenever `FLAG` or `ESC` occurs inside the data payload, an `ESC` byte is prepended. The receiver removes the escape byte upon reception.

- **Bit Stuffing (Bit-Oriented Framing, HDLC / PPP):**
  The flag sequence is strictly `01111110` (six consecutive 1s).
  - **Rule:** Whenever the sender detects five consecutive 1s (`11111`) in the data stream, it unconditionally inserts (stuffs) a `0` bit immediately after the fifth 1.
  - **Receiver Logic:** When five consecutive 1s are encountered:
    - If the next bit is `0`, it is discarded (unstuffed) as an inserted padding bit.
    - If the next bit is `1` followed by `0`, a `FLAG` delimiter is detected (`01111110`).
    - If the next bit is `1` followed by `1`, an error (abort condition) has occurred.

### 2.2 Error Detection: Parity, Checksum & CRC Polynomial Math
Error detection protects frames from channel noise bit-flips without requiring retransmission of all bits.

#### Cyclic Redundancy Check (CRC) Polynomial Division
CRC treats binary data strings as polynomials over Galois Field $GF(2)$ where addition and subtraction are equivalent to the bitwise XOR operation (no carry or borrow).

**Algorithm for Sender Frame Generation:**
1. Let the original data string have $m$ bits.
2. Let the generator polynomial $G(x)$ have degree $r$ (length $r + 1$ bits).
3. Append $r$ zero bits to the end of the data string.
4. Perform binary polynomial division of the appended data by $G(x)$ using XOR subtraction.
5. The $r$-bit remainder is the CRC Checksum (FCS). Replace the appended $r$ zeroes with this remainder to construct the transmitted frame.

**Verification at Receiver:**
The receiver divides the entire received frame by $G(x)$. If the remainder is all zeroes, the frame is error-free; otherwise, a transmission bit error occurred and the frame is discarded.

### 2.3 Flow Control: Stop-and-Wait, Go-Back-N & Selective Repeat
Flow control matches the transmission rate of the sender to the processing speed of the receiver.

Let $T_t = \frac{L}{B}$ be Transmission Time (Packet length $L$ over Bandwidth $B$).  
Let $T_p = \frac{d}{v}$ be Propagation Delay (Distance $d$ over Propagation velocity $v$).  
Let $a = \frac{T_p}{T_t}$ be the propagation-to-transmission ratio.

$$\text{Efficiency } \eta = \frac{N}{1 + 2a}, \quad \text{where } N \text{ is the sender window size}$$

| Protocol | Sender Window Size ($W_s$) | Receiver Window Size ($W_r$) | Sequence Numbers Required ($m$ bits) | Out-of-Order Frames Accepted? | Retransmission Mechanism |
|:---|:---|:---|:---|:---|:---|
| **Stop-and-Wait** | $1$ | $1$ | At least $2$ ($0$ and $1$) | No | Retransmits last unacknowledged frame upon timer expiration. Efficiency: $\frac{1}{1 + 2a}$. |
| **Go-Back-N (GBN)** | $2^m - 1$ | $1$ | $2^m$ | No (Discarded) | Cumulative ACKs. On timeout of frame $k$, retransmits frame $k$ and all subsequent frames in the window. |
| **Selective Repeat (SR)** | $2^{m-1}$ | $2^{m-1}$ | $2^m$ | Yes (Buffered in receiver window) | Individual (Selective) ACKs / NAKs. Retransmits only the single lost or corrupted frame. |

### 2.4 Medium Access Control: CSMA/CD & CSMA/CA
#### Carrier Sense Multiple Access with Collision Detection (CSMA/CD)
Used in legacy half-duplex Ethernet (IEEE 802.3):
1. **Carrier Sense:** Listen before transmit. If channel is busy, wait; if idle, transmit.
2. **Collision Detection:** Listen while transmitting. If signal energy exceeds normal threshold, a collision has occurred.
3. **Jam Signal & Backoff:** If collision detected, transmit a 32-bit Jam signal and execute the **Truncated Binary Exponential Backoff Algorithm**:
   $$K \in [0, 2^{\min(n, 10)} - 1], \quad \text{Wait Time } = K \times 2T_p \text{ (slot time)}$$
   After 16 consecutive collisions ($n = 16$), the transmission is aborted.

**Fundamental CSMA/CD Condition:** The sender must still be transmitting when the collision signal from the farthest possible station arrives back at the sender:
$$T_t \ge 2 \times T_p \implies \frac{L_{\min}}{B} \ge 2 \times \frac{d}{v} \implies L_{\min} \ge 2 \times T_p \times B$$

---

## Chapter 3: Network Layer: IPv4, IPv6, Subnetting & Routing Protocols

### 3.1 IPv4 Header Architecture & Packet Fragmentation
An IPv4 header has a minimum length of 20 bytes (when IHL = 5) and a maximum length of 60 bytes (IHL = 15).

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|     Fragment Offset     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |        Header Checksum        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source IP Address                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination IP Address                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **IHL (Internet Header Length):** 4 bits, measured in 4-byte (32-bit) words. Minimum is 5 ($5 \times 4 = 20\text{ bytes}$).
- **Total Length:** 16 bits, specifies total length of packet (header + payload) in bytes. Maximum packet size $= 2^{16} - 1 = 65,535\text{ bytes}$.
- **Flags (3 bits):**
  - Bit 0: Reserved (must be 0).
  - Bit 1: **DF (Don't Fragment):** If set to 1 and packet > MTU, router drops packet and returns ICMP "Destination Unreachable (Fragmentation Needed)".
  - Bit 2: **MF (More Fragments):** 1 indicates more fragments follow; 0 indicates this is the final fragment.
- **Fragment Offset (13 bits):** Position of fragment payload relative to the original unfragmented packet, measured in **8-byte units** (must be divisible by 8).
- **Time to Live (TTL):** 8 bits, decremented by 1 at every router hop. Prevents infinite looping in routing loops. When TTL reaches 0, router drops packet and sends ICMP "Time Exceeded" (Type 11), the mechanism powering `traceroute`.

### 3.2 CIDR Subnetting Math & VLSM Design
In Classless Inter-Domain Routing (RFC 1519), addresses are written as `a.b.c.d/n`, where `/n` denotes the network prefix length:
- **Network Bits:** $n$
- **Host Bits:** $h = 32 - n$
- **Total Addresses in Block:** $2^h = 2^{32 - n}$
- **Usable Host Addresses:** $2^h - 2$ (Subtracting Network Address where all host bits are `0`, and Directed Broadcast Address where all host bits are `1`).

```
CIDR Prefix Table Reference:
/24 -> 255.255.255.0   -> 2^8  = 256 Total IPs -> 254 Usable Hosts
/25 -> 255.255.255.128 -> 2^7  = 128 Total IPs -> 126 Usable Hosts
/26 -> 255.255.255.192 -> 2^6  = 64  Total IPs -> 62  Usable Hosts
/27 -> 255.255.255.224 -> 2^5  = 32  Total IPs -> 30  Usable Hosts
/28 -> 255.255.255.240 -> 2^4  = 16  Total IPs -> 14  Usable Hosts
/29 -> 255.255.255.248 -> 2^3  = 8   Total IPs -> 6   Usable Hosts
/30 -> 255.255.255.252 -> 2^2  = 4   Total IPs -> 2   Usable Hosts (Point-to-Point links)
```

### 3.3 Address Resolution Protocol (ARP) & NAT/PAT
- **ARP (RFC 826):** Resolves a known Layer 3 logical IP address to a physical Layer 2 MAC address.
  - An ARP Request is a **Broadcast frame** (`FF:FF:FF:FF:FF:FF`) asking: "Who has IP 192.168.1.5? Tell 192.168.1.1".
  - The destination node replies with an **ARP Reply** sent as a **Unicast frame** containing its hardware MAC address.
  - Results are cached in the host's ARP cache table.
- **NAT / PAT (Port Address Translation):** Maps hundreds of private internal IP addresses (RFC 1918: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) to a single public IP address using ephemeral source ports (1024-65535).

### 3.4 Routing Protocols: Distance Vector vs Link State Routing
| Feature | Distance Vector (RIP) | Link State (OSPF) |
|:---|:---|:---|
| **Underlying Algorithm** | Bellman-Ford equation: $D_x(y) = \min_v \{c(x,v) + D_v(y)\}$ | Dijkstra's Shortest Path First (SPF) algorithm |
| **Information Shared** | Vector of distances to all destinations, shared only with immediate direct neighbors. | Entire network topology (Link State Advertisements), flooded to all routers in the AS. |
| **Convergence Speed** | Slow; susceptible to the **Count-to-Infinity problem** when a link fails. | Rapid convergence; updates sent only upon link-state changes. |
| **Loop Prevention** | Split Horizon and Poison Reverse techniques. | Complete graph topology prevents loops mathematically. |

---

## Chapter 4: Transport Layer: TCP Reliability, Flow & Congestion Control

### 4.1 TCP vs UDP Architectural Comparison
| Parameter | Transmission Control Protocol (TCP) | User Datagram Protocol (UDP) |
|:---|:---|:---|
| **Connection Orientation** | Connection-oriented (3-way handshake) | Connectionless (fire and forget) |
| **Reliability** | Guaranteed delivery via ACKs and retransmissions | Best-effort; no retransmission or delivery guarantee |
| **Ordering** | In-order delivery guaranteed via sequence numbers | Unordered arrival; datagrams can arrive out of sequence |
| **Header Overhead** | 20 to 60 bytes | Strictly 8 bytes fixed |
| **Flow & Congestion Control** | Full sliding window and congestion state machines | None; sends packets at rate provided by application |
| **Typical Use Cases** | Web (HTTP/1.1, HTTP/2), Email (SMTP), SSH, File transfers | Streaming video, VoIP, DNS queries, Online gaming, HTTP/3 |

### 4.2 TCP 3-Way Handshake & 4-Way Teardown (TIME_WAIT Deep Dive)

```
        Client                                   Server
          |                                        |
          | ---------- SYN (seq = x) ------------> | (Server enters SYN-RECEIVED)
          | <--- SYN-ACK (seq = y, ack = x + 1) -- | (Client enters ESTABLISHED)
          | ---------- ACK (ack = y + 1) --------> | (Server enters ESTABLISHED)
          |                                        |
      [DATA TRANSFER OCCURS OVER DUPLEX CONNECTION]
          |                                        |
          | ---------- FIN (seq = u) ------------> | (Server enters CLOSE-WAIT)
          | <--------- ACK (ack = u + 1) --------- | (Client enters FIN-WAIT-2)
          | <--------- FIN (seq = v) ------------- | (Server enters LAST-ACK)
          | ---------- ACK (ack = v + 1) --------> | (Server enters CLOSED)
          |                                        |
          | [Client enters TIME_WAIT: 2 * MSL]     |
          | [Expires after 120s -> Enters CLOSED]  |
```

**Why TIME_WAIT is Mandatory (2 * Maximum Segment Lifetime):**
1. **Ensure Final ACK Delivery:** If the client's final ACK is lost in transit, the server retransmits its FIN. The client must still be alive in TIME_WAIT to re-acknowledge the FIN, avoiding a reset `RST`.
2. **Dissipate Old Duplicate Segments:** Prevents stray duplicate packets from the terminated connection from being mistakenly accepted by a new connection reusing the same IP/Port socket 4-tuple.

### 4.3 Sliding Window Flow Control & Silly Window Prevention
- **Flow Control Mechanism:** The receiver advertises its available buffer space via the 16-bit `rwnd` (Receiver Window) field in every TCP header. The sender guarantees that:
  $$\text{Bytes In Flight} \le \min(\text{cwnd}, \text{rwnd})$$
- **Silly Window Syndrome:** If a slow application reads data 1 byte at a time, the receiver window opens by 1 byte, causing the sender to transmit tiny 1-byte packets wrapped in 40-byte TCP/IP headers (overhead > 97%).
  - **Receiver Fix (Clark's Solution):** Prevent advertising small windows until the buffer can receive either a full MSS (Maximum Segment Size) or half the buffer space.
  - **Sender Fix (Nagle's Algorithm):** If unacknowledged data is in flight, buffer outgoing user data until a full MSS accumulates or an ACK arrives.

### 4.4 TCP Congestion Control State Machine
TCP maintains `cwnd` (Congestion Window) and `ssthresh` (Slow Start Threshold):

```
State Machine Transition Flow:
1. Slow Start (cwnd < ssthresh):
   - cwnd initialized to 1 MSS (or initial window 10 MSS in modern Linux).
   - Upon each ACK: cwnd = cwnd + 1 MSS (Doubles cwnd every RTT -> Exponential growth: 1 -> 2 -> 4 -> 8 -> 16).

2. Congestion Avoidance (cwnd >= ssthresh):
   - Upon each RTT: cwnd = cwnd + (1 / cwnd) * 1 MSS (Linear growth: +1 MSS per RTT -> Additive Increase).

3. Packet Loss Event - Triple Duplicate ACKs:
   - Fast Retransmit: Immediately resends the missing segment without waiting for the retransmission timer.
   - Fast Recovery:
     ssthresh = cwnd / 2
     cwnd = ssthresh + 3 MSS (Multiplicative Decrease)
     Continues linear Congestion Avoidance upon new ACK.

4. Packet Loss Event - Retransmission Timeout (RTO):
   - Indicates severe network collapse.
   - ssthresh = cwnd / 2
   - cwnd is reset to 1 MSS
   - Restarts Slow Start from the beginning.
```

---

## Chapter 5: Application Layer Protocols: HTTP, DNS, TLS & WebSockets

### 5.1 The Evolution of Web Protocols: HTTP/1.1 vs HTTP/2 vs HTTP/3
| Architectural Feature | HTTP/1.1 (RFC 2616) | HTTP/2 (RFC 7540) | HTTP/3 (RFC 9114) |
|:---|:---|:---|:---|
| **Transport Layer** | TCP | TCP | **QUIC (UDP)** |
| **Format** | Plaintext ASCII | Binary Framing (Frames & Streams) | Binary Framing |
| **Multiplexing** | No (Head-of-Line blocking on socket; requires multiple parallel TCP connections) | Yes (Multiple streams multiplexed over 1 single TCP connection) | Yes (Independent streams over QUIC; zero cross-stream blocking) |
| **TCP Head-of-Line Blocking** | Present | Present (If 1 TCP packet drops, all multiplexed HTTP streams stall) | **Eliminated** (Packet drop on stream A does not stall stream B) |
| **Connection Setup** | 1 RTT (TCP) + 2 RTT (TLS) = 3 RTT | 1 RTT (TCP) + 1-2 RTT (TLS) | **0-RTT or 1-RTT** (QUIC merges transport and TLS 1.3 handshake) |
| **Connection Migration** | Bound to IP/Port 4-tuple (Disconnects when Wi-Fi switches to LTE) | Bound to IP/Port 4-tuple | Supported via 64-bit Connection ID (survives network IP change) |

### 5.2 Domain Name System (DNS) Architecture
DNS resolves human-readable domain names (`recruiter.ai.edu`) into IP addresses (`142.250.190.46`). It uses UDP port 53 (and TCP port 53 for zone transfers > 512 bytes).

**Recursive Query vs Iterative Query Pathway:**
```
[Client Browser]
      |  (1) Recursive Query: "What is IP of recruiter.ai.edu?"
      v
[Local DNS Resolver / ISP (e.g., 8.8.8.8)]
      |  (2) Iterative Query: "recruiter.ai.edu"
      v
[Root Nameserver (13 logical root server clusters: a.root-servers.net)]
      |  (3) Referral: "Ask the .edu TLD server at IP x.x.x.x"
      v
[TLD Nameserver (.edu)]
      |  (4) Referral: "Ask the ai.edu Authoritative server at IP y.y.y.y"
      v
[Authoritative Nameserver (ai.edu)]
      |  (5) Answer: "recruiter.ai.edu has A record 142.250.190.46 (TTL=300)"
      v
[Local DNS Resolver Caches Result & Returns to Browser]
```

### 5.3 Transport Layer Security (TLS 1.3) Cryptographic Handshake
TLS 1.3 (RFC 8446) reduced the handshake latency from 2 RTTs (in TLS 1.2) to **1 RTT**:

1. **ClientHello:** Sends supported cipher suites, TLS version (1.3), random nonce, and the **Client Diffie-Hellman Key Share** ($g^a \bmod p$) using Elliptic Curve Cryptography (ECDHE).
2. **ServerHello:** Selects the cipher suite, sends Server random nonce, and the **Server Key Share** ($g^b \bmod p$).
   - Both client and server immediately derive the shared symmetric encryption key ($g^{ab} \bmod p$).
   - The server encrypts all subsequent handshake messages with this key.
3. **Encrypted Server Payload:** Server sends its X.509 Digital Certificate, Digital Signature over the handshake transcript, and `Finished` MAC.
4. **Client Verification:** Client verifies the server certificate against local Root Certificate Authorities (CA), validates the signature, and sends its `Finished` MAC.
5. Secure encrypted application data exchange begins.

### 5.4 WebSockets Full-Duplex Real-Time Communication
HTTP is unidirectional and request-driven. WebSockets (RFC 6455) provides persistent, bi-directional, full-duplex communication over a single TCP connection:
- Initiated via an standard HTTP/1.1 request containing headers:
  ```http
  GET /chat HTTP/1.1
  Host: server.example.com
  Upgrade: websocket
  Connection: Upgrade
  Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
  Sec-WebSocket-Version: 13
  ```
- If the server accepts, it responds with status `101 Switching Protocols`:
  ```http
  HTTP/1.1 101 Switching Protocols
  Upgrade: websocket
  Connection: Upgrade
  Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
  ```
- From this moment on, HTTP semantics are dropped and both parties exchange lightweight binary/text frames with only 2 to 10 bytes of frame framing overhead.

---

## Chapter 6: Solved Networking Placement Numericals & Interview Drills

### Solved Problem 1: CIDR VLSM Subnet Allocation
- **Problem:** An organization has been assigned the network block `172.16.0.0/22`. Design a Variable Length Subnet Mask (VLSM) scheme to allocate subnets for 3 separate departments:
  - Department A: 450 hosts
  - Department B: 200 hosts
  - Department C: 100 hosts
  Determine the subnet mask, network address, usable host IP range, and broadcast address for each department.
- **Solution:**
  1. **Department A (450 hosts):**
     - Host bits needed: $2^h - 2 \ge 450 \implies 2^9 - 2 = 510 \ge 450 \implies h = 9$.
     - Subnet prefix: $32 - 9 = \mathbf{/23}$. Subnet mask: `255.255.254.0`.
     - Network ID: `172.16.0.0/23`.
     - Usable Host Range: `172.16.0.1` to `172.16.1.254`.
     - Directed Broadcast Address: `172.16.1.255`.
     - Total addresses consumed: $2^9 = 512$ (spans `172.16.0.0` - `172.16.1.255`).
  2. **Department B (200 hosts):**
     - Next available network address: `172.16.2.0`.
     - Host bits needed: $2^h - 2 \ge 200 \implies 2^8 - 2 = 254 \ge 200 \implies h = 8$.
     - Subnet prefix: $32 - 8 = \mathbf{/24}$. Subnet mask: `255.255.255.0`.
     - Network ID: `172.16.2.0/24`.
     - Usable Host Range: `172.16.2.1` to `172.16.2.254`.
     - Directed Broadcast Address: `172.16.2.255`.
     - Total addresses consumed: $2^8 = 256$ (spans `172.16.2.0` - `172.16.2.255`).
  3. **Department C (100 hosts):**
     - Next available network address: `172.16.3.0`.
     - Host bits needed: $2^h - 2 \ge 100 \implies 2^7 - 2 = 126 \ge 100 \implies h = 7$.
     - Subnet prefix: $32 - 7 = \mathbf{/25}$. Subnet mask: `255.255.255.128`.
     - Network ID: `172.16.3.0/25`.
     - Usable Host Range: `172.16.3.1` to `172.16.3.126`.
     - Directed Broadcast Address: `172.16.3.127`.

### Solved Problem 2: CRC-32 Frame Generation & Check
- **Problem:** Data bit sequence $M = 1101011011$. Generator polynomial $G(x) = x^4 + x + 1$ (bit string `10011`). Compute the transmitted CRC codeword.
- **Solution:**
  1. Degree of $G(x)$ is $r = 4$. Append 4 zeros to data $M$: `11010110110000`.
  2. Perform polynomial division using XOR:
     ```
     11010110110000 / 10011
     11010110110000
     10011
     -----
     010011
      10011
      -----
      0000010110
            10011
            -----
            0010100
              10011
              -----
              001110
                10011
                -----
                01101 (Remainder is 1110 -> 4 bits)
     ```
  3. The 4-bit remainder (FCS) is `1110`.
  4. Transmitted frame codeword: `11010110111110`.

### Solved Problem 3: CSMA/CD Minimum Packet Size Determination
- **Problem:** A 1 Gbps ($10^9\text{ bps}$) half-duplex CSMA/CD Ethernet network has a cable length of 1 km with signal propagation speed $v = 2 \times 10^8\text{ m/s}$. Determine the minimum Ethernet frame size in bytes.
- **Solution:**
  1. Propagation time: $T_p = \frac{\text{Distance}}{v} = \frac{1000\text{ m}}{2 \times 10^8\text{ m/s}} = 5 \times 10^{-6}\text{ s} = 5\ \mu\text{s}$.
  2. Round-Trip Time: $2 \times T_p = 2 \times 5\ \mu\text{s} = 10\ \mu\text{s} = 10^{-5}\text{ s}$.
  3. For CSMA/CD collision detection:
     $$T_t \ge 2 T_p \implies \frac{L_{\min}}{\text{Bandwidth}} \ge 2 T_p$$
     $$L_{\min} = 2 \times T_p \times B = 10^{-5}\text{ s} \times 10^9\text{ bps} = 10^4\text{ bits}$$
  4. Frame size in bytes: $L_{\min} = \frac{10,000}{8} = \mathbf{1250\text{ bytes}}$.

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (TCP Sequence Arithmetic):** Host A sends 3 consecutive TCP segments of size 1460 bytes each to Host B. If the initial sequence number of the first segment is 5000, what is the sequence number and acknowledgment number in Host B's response acknowledging all three segments?
   - *Solution:* First segment spans bytes [5000 to 6459]. Second segment spans bytes [6460 to 7919]. Third segment spans bytes [7920 to 9379]. Host B acknowledges the next expected byte: $\text{ACK} = 9380$.

2. **Exercise 2 (Subnet Capacity):** What is the maximum number of usable host IP addresses in a `/21` IPv4 network?
   - *Solution:* Host bits $h = 32 - 21 = 11$. Total hosts $= 2^{11} - 2 = 2048 - 2 = \mathbf{2046\text{ usable hosts}}$.

3. **Exercise 3 (HTTP/2 vs HTTP/3):** What fundamental transport-layer limitation causes HTTP/2 to experience Head-of-Line blocking, and how does HTTP/3 overcome it?
   - *Solution:* HTTP/2 multiplexes all logical streams over a single TCP byte-stream. If one TCP packet is dropped, TCP halts delivery of all subsequent data across all streams until the missing segment is retransmitted. HTTP/3 runs on top of QUIC (UDP), where each stream maintains its own independent sequence tracking; a dropped packet in stream A has zero impact on streams B and C.

4. **Exercise 4 (Selective Repeat Window Size):** If 4 bits are allocated for sequence numbers in the frame header, what is the maximum permissible sender window size in Selective Repeat protocol to prevent duplicate frame ambiguity?
   - *Solution:* Condition for Selective Repeat: $W_s + W_r \le 2^m$. Since $W_s = W_r$, $2 W_s \le 2^m \implies W_s \le 2^{m-1} = 2^{4-1} = 2^3 = \mathbf{8}$.

5. **Exercise 5 (NAT Port Range):** Why does Port Address Translation (PAT) support up to approximately 64,000 concurrent outbound connections per public IP address?
   - *Solution:* TCP source port is a 16-bit field ($2^{16} = 65,536$ possible ports). Excluding the well-known reserved system ports (0 to 1023), approximately 64,512 ephemeral ports are available for NAT translation mappings.
"""

CN_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 3,
        "chapter_title": "Network Layer: IPv4, IPv6, Subnetting & Routing Protocols",
        "subtopic": "Subnet Host Capacity",
        "question": "How many usable host IP addresses are available in a subnetwork with CIDR prefix /27?",
        "options": ["30", "32", "62", "28"],
        "correct_option_index": 0,
        "explanation": "📖 [CN Prescribed Textbook — Chapter 3: Network Layer & Subnetting]\nAn IPv4 address has 32 bits. For /27, remaining host bits = 32 - 27 = 5 bits. Total IP addresses = 2^5 = 32. Subtracting 2 (Network ID and Directed Broadcast Address) leaves exactly 30 usable host addresses.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 4,
        "chapter_title": "Transport Layer: TCP Reliability, Flow & Congestion Control",
        "subtopic": "TCP Congestion Window Growth",
        "question": "In TCP Congestion Control, how does the Congestion Window (cwnd) grow during the Slow Start phase upon receiving successful acknowledgments?",
        "options": [
            "Exponentially (doubles every Round-Trip Time)",
            "Linearly (increases by 1 MSS every RTT)",
            "Logarithmically (increases by log(cwnd))",
            "Remains constant until reaching maximum bandwidth"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [CN Prescribed Textbook — Chapter 4: Transport Layer]\nDuring Slow Start, cwnd increases by 1 MSS for every received ACK, which results in doubling the window size every RTT (exponential growth) until it hits the slow start threshold (ssthresh).",
        "difficulty": "medium",
    },
    {
        "chapter_num": 2,
        "chapter_title": "Data Link Layer, Framing & Error Control Protocols",
        "subtopic": "CSMA/CD Minimum Frame Size",
        "question": "In a CSMA/CD Ethernet network, why must the minimum transmission time of a frame be at least twice the propagation delay (Tt >= 2*Tp)?",
        "options": [
            "To ensure the sender is still transmitting when a collision signal from the farthest node returns, allowing detection",
            "To prevent the receiver buffer from overflowing",
            "To allow the router to calculate the CRC polynomial",
            "To encrypt the packet with TLS 1.3"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [CN Prescribed Textbook — Chapter 2: Data Link Layer & CSMA/CD]\nIn CSMA/CD, the transmitting station can only detect collisions while it is actively sending bits. If the frame is shorter than 2*Tp, the sender finishes sending before the collision wave arrives back, failing to detect the corrupted packet.",
        "difficulty": "hard",
    }
]
