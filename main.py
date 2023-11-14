import conf
import worker_results
import worker_tests

alpha = 0.01
only_manual = False

def main():
    for domain in conf.Domains:
        results_domain = worker_results.ResultsDomain(domain, ony_manual=only_manual)
        tests_domain = worker_tests.TestsDomain(domain, alpha)
    tests_domains = worker_tests.TestsDomains(alpha)

if __name__ == '__main__':
    main()