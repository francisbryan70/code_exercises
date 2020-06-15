import datetime

class Cov():
    def __init__(self, eff, term):
        self.eff = eff
        self.term = term

    # Used to display print out object details
    def __str__(self):
        return (f'{self.__class__.__name__}('
                f'{self.eff!r}, {self.term!r})')

    # Used to see object details when debugging
    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.eff!r}, {self.term!r})')

    # Determine max coverage length
    def coverage_length(self):
        coverage_length = self.term - self.eff + 1
        return coverage_length

    # Coverage day numbers to dates
    def coverage_dates(self):
        # Determine Current_Year
        # 2020 is a Leap Year
        year = datetime.date.today().year
        start_of_year = datetime.datetime(year, 1, 1)

        # Subtract 1 from start_date_delta and end_date_delta
        # becuase we are starting at 1/1/Current_Year or day 1
        start_date_delta = datetime.timedelta(days=self.eff - 1)
        end_date_delta = datetime.timedelta(days=self.term - 1)
        start_day = start_of_year + start_date_delta
        end_day = start_of_year + end_date_delta
        start_day_string = start_day.strftime('%m-%d-%Y')
        end_day_string = end_day.strftime('%m-%d-%Y')

        return start_day_string, end_day_string


if __name__ == '__main__':
    # Assumtions:
    # Cov(1,20) = 20 Day(s); Start Date = 01-01-2020 - End Date = 01-20-2020
    #
    # Cov(1,365) would mean there is coverage from 1/1 = 12/31 on a non leap year
    # Cov(1,366) would mean there is coverage from 1/1 = 12/31 on a leap year
    # 2020 is a Leap Year
    #
    # Consecutive coverages do not result in a gap in coverage
    # Cov(1,20), Cov(21, 30) has the same coverage length of Cov(1, 30)
    #
    # If two coverage periods are equal [Cov(1,20), Cov(31,50)]
    # Output should reflect that there are to coverage periods equaling the max coverage

    # Test Cases
    # Empty List
    #coverages = []
    # Leap Year
    #coverages = [Cov(1, 365), Cov(1, 366)]
    # Continuous / Consecutive Coverages
    #coverages = [Cov(1, 20), Cov(21, 30)]
    # Two Coverage periods with the same length
    #coverages = [Cov(1, 20), Cov(31, 50)]
    # Max length at start of list
    #coverages = [Cov(1, 50), Cov(90, 95)]
    # Max lenght at end list
    #coverages = [Cov(1, 5), Cov(90, 120)]
    # Test Sort order
    #coverages = [Cov(50, 60), Cov(61, 70), Cov(1, 28), Cov(20, 38), Cov(35, 48), Cov(81, 128)]

    # Exercise Data
    coverages = [Cov(1, 20), Cov(21, 30), Cov(28, 40), Cov(50,60), Cov(61, 200)]


    # Sort coverages for processing
    sorted_coverages = sorted(coverages, key=lambda item: item.eff)

    longest_coverage = 0

    # max_coverage_list will contain tuples consisting of
    # (coverage_length, cov_object_for_coverage_period, cov_making_up_cov_period)
    max_coverage_list = []

    if sorted_coverages:

        current_cov_period = None
        covs_in_current_cov_period = []

        for cov in sorted_coverages:
            if current_cov_period is None:
                current_cov_period = Cov(cov.eff, cov.term)
                covs_in_current_cov_period.append(cov)
            else:
                if current_cov_period.term + 1 >= cov.eff:
                    covs_in_current_cov_period.append(cov)
                    if current_cov_period.term < cov.term:
                        current_cov_period.term = cov.term
                else:
                    max_coverage_list.append((current_cov_period.coverage_length(),
                                             current_cov_period, covs_in_current_cov_period.copy()))

                    if longest_coverage < current_cov_period.coverage_length():
                        longest_coverage = current_cov_period.coverage_length()

                    current_cov_period = Cov(cov.eff, cov.term)
                    covs_in_current_cov_period.clear()
                    covs_in_current_cov_period.append(cov)

        # Store last current_cov_period from iteration of for loop
        max_coverage_list.append((current_cov_period.coverage_length(),
                                 current_cov_period, covs_in_current_cov_period.copy()))

        if longest_coverage < current_cov_period.coverage_length():
            longest_coverage = current_cov_period.coverage_length()

        # Fitler out coverage periods that don't have the max coverage length
        max_coverage_list = list(filter(lambda cov: cov[0] == longest_coverage, max_coverage_list))

# Print results
# Longest Continuous Coverage
print(f'Longest Continuous Coverage = {longest_coverage} day(s)')
print()
if max_coverage_list:
    # How many coverage periods had a max length
    print(f'There was/were {len(max_coverage_list)} coverage period(s) with a max length = {longest_coverage} day(s)')
    print()
    # Details of coverage periods
    for i, period in enumerate(max_coverage_list):
        p_start_day, p_end_day = period[1].coverage_dates()
        print(f'Coverage Period {i + 1} - {period[1]}: {period[1].coverage_length()} Days : {p_start_day} to {p_end_day}')
        print(f'Coverages included in Coverage Period {i + 1}:')
        for c in period[2]:
            c_start_day, c_end_day = c.coverage_dates()
            print(f'- {c}: {c.coverage_length()} Days : {c_start_day} to {c_end_day}')
        print()
