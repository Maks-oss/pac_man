(import pandas :as pd)
(import numpy :as np)
(import math :as ma)

(setv file (pd.read_csv "results.csv"))
(setv times (np.array (file.drop ["Won" "Score"] :axis 1)))
(setv reshaped (times.flatten))
(setv count_array (np.arange 1 12))
(setv sum 0)
(for [i count_array]
      (setv sum (+ sum (* (. reshaped [(- i 1)]) i)))
)
(print "Mathematical Expectation of time quantity: " sum)

(setv scores (np.array (file.drop ["Time" "Won"] :axis 1)))
(setv reshaped (scores.flatten))
(setv m_x_double 0)
(setv m_x 0)
(for [i count_array]
      (setv m_x_double (+ m_x_double (* (. reshaped [(- i 1)]) (ma.pow i 2))))
      (setv m_x (+ m_x (* (. reshaped [(- i 1)]) i)))
)
(setv dispersion (- m_x_double (ma.pow m_x 2)))
(print "Mathematical Dispersion of points: "dispersion)